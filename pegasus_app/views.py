from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from pegasus_app.forms import PhoneForm, ScheduleForm, ScheduleFormset
from pegasus_app.models import Schedule, Phone


class PhoneView(TemplateView):
    model = Phone
    template_name = 'phone_create.html'
    form_class = PhoneForm
    formset_class = ScheduleFormset
    object = None

    def get_form_and_formset(self):
        obj_id = self.kwargs.get('phone_id', None)
        obj = self.model.objects.filter(id=obj_id).first()

        form_kwargs = {'instance': obj}
        if self.request.method in ('POST', 'PUT'):
            form_kwargs.update({'data': self.request.POST})
        form = self.form_class(**form_kwargs)

        formset_kwargs = form_kwargs.copy()
        if self.request.method == 'GET':
            initial = [{'day': day_value} for day_value in Schedule.Day.values]
            formset_kwargs.update({'initial': initial})
        formset = self.formset_class(**formset_kwargs)

        return form, formset

    def get(self, request, *args, **kwargs):
        phones_data = Phone.objects.all()

        """
        Handles GET requests and instantiates blank versions of the phone_form
        and its inline formsets.
        """

        phone_form, schedule_formset = self.get_form_and_formset()
        context = self.get_context_data(phone_form=phone_form, schedule_formset=schedule_formset, phones_data=phones_data)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        phones_numbers = Phone.objects.values_list('number')
        count_of_numbers = len(phones_numbers)
        max_phones_numbers = request.user.plan.max_phones_numbers

        if count_of_numbers >= max_phones_numbers:
            raise ValidationError(
                "You cannot create a number. Pay attention to your Plan"
            )

        """
        Handles POST requests, instantiating a phone_form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        phone_form, schedule_formset = self.get_form_and_formset()

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
