from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from pegasus_app.forms import PhoneNumberCheckConfigForm, ScheduleDayForm, ScheduleDayFormset
from pegasus_app.models import Schedule, Phone


class PhoneNumberCheckConfigCreateView(CreateView):
    model = Phone
    template_name = 'phone_create.html'
    form_class = PhoneNumberCheckConfigForm
    object = None

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        weekday_formset = ScheduleDayFormset()
        return self.render_to_response(
            self.get_context_data(phone_form=form,
                                  weekday_formset=weekday_formset,
                                  )
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a phone_form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        phone_form = self.get_form(form_class)
        schedule_day_formset = ScheduleDayFormset(self.request.POST)
        if phone_form.is_valid() and schedule_day_formset.is_valid():
            return self.forms_valid(phone_form, schedule_day_formset)
        else:
            return self.forms_invalid(phone_form, schedule_day_formset)

    def forms_valid(self, phone_form, schedule_day_formset):
        """
        Called if all forms are valid. Creates Assignment instance along with the
        associated AssignmentQuestion instances then redirects to success url
        Args:
            phone_form: Assignment Form
            schedule_day_formset: Assignment Question Form

        Returns: an HttpResponse to success url

        """
        self.object = phone_form.save(commit=False)
        # pre-processing for Assignment instance here...
        self.object.save()

        # saving AssignmentQuestion Instances
        schedule_days = schedule_day_formset.save(commit=False)
        for schedule_day in schedule_days:
            #  change the AssignmentQuestion instance values here
            #  schedule_day.some_field = some_value
            schedule_day.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, phone_form, schedule_day_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            phone_form: Phone Form
            schedule_day_formset: Schedule Schedule Form
        """
        return self.render_to_response(
            self.get_context_data(phone_form=phone_form,
                                  schedule_day_formset=schedule_day_formset
                                  )
        )


def get_schedule_day_form(phone_config, weekday):
    schedule_day = Schedule.objects.filter(phone_config=phone_config, day=weekday).first()

    return ScheduleDayForm(instance=schedule_day, prefix=weekday)


def validate_and_save_schedule_day_form(payload, phone_config, weekday):
    schedule_day_form = ScheduleDayForm(payload, prefix=weekday)
    if schedule_day_form.is_valid():
        Schedule.objects.update_or_create(
            phone_config=phone_config,
            day=weekday,
            defaults=schedule_day_form.cleaned_data
        )
    return schedule_day_form


def schedule_form_handler(request, phone_config, weekday):
    if request.method == 'GET':
        schedule_day = Schedule.objects.filter(phone_config=phone_config, day=weekday).first()
        schedule_day_form = ScheduleDayForm(instance=schedule_day, prefix=weekday)
    elif request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        schedule_day_form = ScheduleDayForm(request.POST, prefix=weekday)
        if schedule_day_form.is_valid():
            if schedule_day_form.cleaned_data['is_active']:
                Schedule.objects.update_or_create(
                    phone_config=phone_config,
                    day=weekday,
                    defaults=schedule_day_form.cleaned_data
                )
            # else:
            #     Schedule.objects.update_or_create(
            #         phone=phone,
            #         day=weekday,
            #         defaults={
            #             'open_time': None,
            #             'close_time': None,
            #         }
            #     )
    return schedule_day_form


def change_config_number(request, id):
    phone_config = Phone.objects.get(id=id)
    if request.method == 'GET':
        schedule_day_formset = ScheduleDayFormset(phone_config=phone_config, )

        #
        # schedule_monday_form = get_schedule_day_form(phone, Schedule.Day.MONDAY)
        # schedule_tuesday_form = get_schedule_day_form(phone, Schedule.Day.TUESDAY)
        # schedule_wednesday_form = get_schedule_day_form(phone, Schedule.Day.WEDNESDAY)
        # schedule_thursday_form = ScheduleDayForm(instance=schedule_thursday, prefix='thursday')
        # schedule_friday_form = ScheduleDayForm(instance=schedule_friday, prefix='friday')
        # schedule_saturday_form = ScheduleDayForm(instance=schedule_saturday, prefix='saturday')
        # schedule_sunday_form = ScheduleDayForm(instance=schedule_sunday, prefix='sunday')

    elif request.method == 'POST':

        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        if phone_config_form.is_valid():
            Phone.objects.update_or_create(id=id, defaults={
                'ima_name': phone_config_form.cleaned_data['ima_name'],
                'number': phone_config_form.cleaned_data['number'],
                'failure_threshold': phone_config_form.cleaned_data['failure_threshold'],
                'test_frequency': phone_config_form.cleaned_data['test_frequency']
            })

        # schedule_monday_form = validate_and_save_schedule_day_form(
        #     request.POST, phone, Schedule.Day.MONDAY
        # )
        # ...

    context = {
        'phone_config_form': phone_config_form,
        'schedule_day_formset': schedule_day_formset
        # 'schedule_tuesday_form': schedule_form_handler(request, phone, Schedule.Day.TUESDAY),
        # 'schedule_wednesday_form': schedule_form_handler(request, phone, Schedule.Day.WEDNESDAY),
        # 'schedule_thursday_form': schedule_form_handler(request, phone, Schedule.Day.THURSDAY),
        # 'schedule_friday_form': schedule_form_handler(request, phone, Schedule.Day.FRIDAY),
        # 'schedule_saturday_form': schedule_form_handler(request, phone, Schedule.Day.SATURDAY),
        # 'schedule_sunday_form': schedule_form_handler(request, phone, Schedule.Day.SUNDAY)

    }

    return render(request, 'pegasus_app/change_number.html', context)


def home_page(request):
    phone_config_form = PhoneNumberCheckConfigForm()
    phone = Phone.objects.values('number')
    schedule_formset = ScheduleDayFormset()
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        schedule_formset = ScheduleDayFormset(request.POST)
        if phone_config_form.is_valid():
            phone_config = phone_config_form.save(commit=False)
            phone_config.user_plan = request.user.plan
            phone_config.save()
            for form in schedule_formset:
                if form.is_valid():
                    form.cleaned_data['phone'] = phone_config
                    schedule_day = Schedule.objects.create(**form.cleaned_data)

    print(request.POST)

    context = {
        'number': phone,
        'phone_config_form': phone_config_form,
        'schedule_formset': schedule_formset
    }

    return render(request, 'pegasus_app/main.html', context)


class Phone(TemplateView):
    template_name = "temp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phone_number = Phone.objects.first()
        phone_number_form = PhoneNumberCheckConfigForm(instance=phone_number)
        context['phone_number_form'] = phone_number_form

        schedule_formset = ScheduleDayFormset(instance=phone_number)
        context['schedule_formset'] = schedule_formset

        return context

    def post(self, request, id):
        phone_number = Phone.objects.get(id=id)
        # import ipdb; ipdb.set_trace()
        phone_number_form = PhoneNumberCheckConfigForm(instance=phone_number, data=request.POST)
        if phone_number_form.is_valid():
            phone_number_form.save()

        formset = ScheduleDayFormset(request.POST, instance=phone_number)
        if formset.is_valid():
            formset.save()

        redirect_url = reverse('phone', args='1')
        return HttpResponseRedirect(redirect_url)


def manage_books(request, author_id):
    author = Author.objects.get(pk=author_id)
    BookInlineFormSet = inlineformset_factory(Author, Book, fields=('title',))
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(author.get_absolute_url())
    else:
        formset = BookInlineFormSet(instance=author)
    return render(request, 'manage_books.html', {'formset': formset})
