from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView

from pegasus_app.forms import PhoneNumberCheckConfigForm, ScheduleDayForm, ScheduleDayFormset
from pegasus_app.models import ScheduleDay, PhoneNumberCheckConfig


def get_schedule_day_form(phone_config, weekday):
    schedule_day = ScheduleDay.objects.filter(phone_config=phone_config,day=weekday).first()

    return ScheduleDayForm(instance=schedule_day, prefix=weekday)


def validate_and_save_schedule_day_form(payload, phone_config, weekday):
    schedule_day_form = ScheduleDayForm(payload, prefix=weekday)
    if schedule_day_form.is_valid():
        ScheduleDay.objects.update_or_create(
            phone_config=phone_config,
            day=weekday,
            defaults=schedule_day_form.cleaned_data
        )
    return schedule_day_form


def schedule_form_handler(request, phone_config, weekday):
    if request.method == 'GET':
        schedule_day = ScheduleDay.objects.filter(phone_config=phone_config, day=weekday).first()
        schedule_day_form = ScheduleDayForm(instance=schedule_day, prefix=weekday)
    elif request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        schedule_day_form = ScheduleDayForm(request.POST, prefix=weekday)
        if schedule_day_form.is_valid():
            if schedule_day_form.cleaned_data['is_active']:
                ScheduleDay.objects.update_or_create(
                    phone_config=phone_config,
                    day=weekday,
                    defaults=schedule_day_form.cleaned_data
                )
            # else:
            #     ScheduleDay.objects.update_or_create(
            #         phone_config=phone_config,
            #         day=weekday,
            #         defaults={
            #             'open_time': None,
            #             'close_time': None,
            #         }
            #     )
    return schedule_day_form


def change_config_number(request, id):
    phone_config = PhoneNumberCheckConfig.objects.get(id=id)
    if request.method == 'GET':
        phone_config_form = PhoneNumberCheckConfigForm(instance=phone_config)
        #
        # schedule_monday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.MONDAY)
        # schedule_tuesday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.TUESDAY)
        # schedule_wednesday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.WEDNESDAY)
        # schedule_thursday_form = ScheduleDayForm(instance=schedule_thursday, prefix='thursday')
        # schedule_friday_form = ScheduleDayForm(instance=schedule_friday, prefix='friday')
        # schedule_saturday_form = ScheduleDayForm(instance=schedule_saturday, prefix='saturday')
        # schedule_sunday_form = ScheduleDayForm(instance=schedule_sunday, prefix='sunday')

    elif request.method == 'POST':

        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        if phone_config_form.is_valid():
            PhoneNumberCheckConfig.objects.update_or_create(id=id, defaults={
                'ima_name': phone_config_form.cleaned_data['ima_name'],
                'phone': phone_config_form.cleaned_data['phone'],
                'failure_threshold': phone_config_form.cleaned_data['failure_threshold'],
                'test_frequency': phone_config_form.cleaned_data['test_frequency']
            })

        # schedule_monday_form = validate_and_save_schedule_day_form(
        #     request.POST, phone_config, ScheduleDay.ScheduleDayType.MONDAY
        # )
        # ...

    context = {
        'phone_config_form': phone_config_form,
        'schedule_monday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.MONDAY),
        'schedule_tuesday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.TUESDAY),
        'schedule_wednesday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.WEDNESDAY),
        'schedule_thursday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.THURSDAY),
        'schedule_friday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.FRIDAY),
        'schedule_saturday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.SATURDAY),
        'schedule_sunday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.SUNDAY)

    }

    return render(request, 'pegasus_app/change_number.html', context)


def home_page(request):
    phone_config_form = PhoneNumberCheckConfigForm()
    phone = PhoneNumberCheckConfig.objects.values('phone')
    if request.method == 'POST':
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        schedule_formset = ScheduleDayForm(request.POST)
        if phone_config_form.is_valid():
            phone_config = phone_config_form.save(commit=False)
            phone_config.user_plan = request.user.plan
            phone_config.save()
            for form in schedule_formset:
                if form.is_valid():
                    form.cleaned_data['phone_config'] = phone_config
                    schedule_day = ScheduleDay.objects.create(**form.cleaned_data)

    print(request.POST)

    context = {
        'phone': phone,
        'phone_config_form': phone_config_form,
        'schedule_monday_form': ScheduleDayForm(),
        'schedule_tuesday_form': ScheduleDayForm(),
        'schedule_wednesday_form': ScheduleDayForm(),
        'schedule_thursday_form': ScheduleDayForm(),
        'schedule_friday_form': ScheduleDayForm(),
        'schedule_saturday_form': ScheduleDayForm(),
        'schedule_sunday_form': ScheduleDayForm()
    }

    return render(request, 'pegasus_app/main.html', context)


class TempView(TemplateView):
    template_name = "temp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phone_number = PhoneNumberCheckConfig.objects.first()
        phone_number_form = PhoneNumberCheckConfigForm(instance=phone_number)
        context['phone_number_form'] = phone_number_form

        schedule_formset = ScheduleDayFormset(instance=phone_number)
        context['schedule_formset'] = schedule_formset

        return context
