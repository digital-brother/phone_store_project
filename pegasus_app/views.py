from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from pegasus_app.forms import PhoneForm, ScheduleFormset
from pegasus_app.models import Schedule, Phone


class PhoneBaseView(TemplateView):
    model = Phone
    template_name = None  # Should be set in inheritors
    form_class = PhoneForm
    formset_class = ScheduleFormset

    object = None

    def get_object(self):
        obj_id = self.kwargs.get('phone_id', None)
        obj = self.model.objects.filter(id=obj_id).first()
        return obj

    def get_form(self):
        obj = self.get_object()

        form_kwargs = {'instance': obj}
        if self.request.method in ('POST', 'PUT'):
            form_data = self.request.POST.copy()
            form_data['owner'] = self.request.user
            form_kwargs.update({'data': form_data})
        form = self.form_class(**form_kwargs)

        return form

    def get_formset(self):
        obj = self.get_object()

        formset_kwargs = {'instance': obj}
        if self.request.method == 'GET':
            initial = [{'day': day_value} for day_value in Schedule.Day.values]
            formset_kwargs.update({'initial': initial})
        elif self.request.method in ('POST', 'PUT'):
            formset_kwargs.update({'data': self.request.POST})
        formset = self.formset_class(**formset_kwargs)

        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phones_data = self.request.user.phones.all()
        context['phones_data'] = phones_data

        max_count_numbers = self.request.user.plan.max_phones_numbers
        context['max_count_numbers'] = max_count_numbers

        return context

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the phone_form
        and its inline formsets.
        """
        phone_form = self.get_form()
        schedule_formset = self.get_formset()
        context = self.get_context_data(phone_form=phone_form, schedule_formset=schedule_formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a phone_form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        phone_form = self.get_form()
        schedule_formset = self.get_formset()

        if phone_form.is_valid() and schedule_formset.is_valid():
            return self.forms_valid(phone_form, schedule_formset)
        else:
            return self.forms_invalid(phone_form, schedule_formset)

    def forms_valid(self, phone_form, schedule_formset):
        """
        Called if all forms are valid. Creates Assignment instance along with the
        associated AssignmentQuestion instances then redirects to success url
        """
        phone = phone_form.save()

        # schedule formset is saved by hands, otherwise raises
        # "save() prohibited to prevent data loss due to unsaved related object"
        schedules = schedule_formset.save(commit=False)
        for schedule in schedules:
            schedule.phone = phone
            schedule.save()

        schedule_formset.save_m2m()

        success_url = reverse('phone_edit', kwargs={'phone_id': phone.id})
        return HttpResponseRedirect(success_url)

    def forms_invalid(self, phone_form, schedule_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        context = self.get_context_data(phone_form=phone_form, schedule_formset=schedule_formset)
        return self.render_to_response(context)


class PhoneCreateView(PhoneBaseView):
    template_name = 'pegasus_app/phone_create.html'


class PhoneEditView(PhoneBaseView):
    template_name = 'pegasus_app/phone_edit.html'
