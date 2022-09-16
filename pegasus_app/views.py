from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView

from pegasus_app.forms import PhoneNumberCheckConfigForm, ScheduleDayForm
from pegasus_app.models import ScheduleDay, PhoneNumberCheckConfig


def change_config_number(request, id):
    phone_config = PhoneNumberCheckConfig.objects.get(id=id)
    if request.method == 'GET':
        schedule_monday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                     day=ScheduleDay.ScheduleDayType.MONDAY).first()
        schedule_tuesday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                      day=ScheduleDay.ScheduleDayType.TUESDAY).first()
        schedule_wednesday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                        day=ScheduleDay.ScheduleDayType.WEDNESDAY).first()
        schedule_thursday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                       day=ScheduleDay.ScheduleDayType.THURSDAY).first()
        schedule_friday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                     day=ScheduleDay.ScheduleDayType.FRIDAY).first()
        schedule_saturday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                       day=ScheduleDay.ScheduleDayType.SATURDAY).first()
        schedule_sunday = ScheduleDay.objects.filter(phone_config=phone_config,
                                                     day=ScheduleDay.ScheduleDayType.SUNDAY).first()

        phone_config_form = PhoneNumberCheckConfigForm(instance=phone_config)
        schedule_monday_form = ScheduleDayForm(instance=schedule_monday, prefix='monday')
        schedule_tuesday_form = ScheduleDayForm(instance=schedule_tuesday, prefix='tuesday')
        schedule_wednesday_form = ScheduleDayForm(instance=schedule_wednesday, prefix='wednesday')
        schedule_thursday_form = ScheduleDayForm(instance=schedule_thursday, prefix='thursday')
        schedule_friday_form = ScheduleDayForm(instance=schedule_friday, prefix='friday')
        schedule_saturday_form = ScheduleDayForm(instance=schedule_saturday, prefix='saturday')
        schedule_sunday_form = ScheduleDayForm(instance=schedule_sunday, prefix='sunday')

    elif request.method == 'POST':
        import ipdb; ipdb.set_trace()
        schedule_monday_form = ScheduleDayForm(request.POST, prefix='monday')
        schedule_tuesday_form = ScheduleDayForm(request.POST, prefix='tuesday')
        schedule_wednesday_form = ScheduleDayForm(request.POST, prefix='wednesday')
        schedule_thursday_form = ScheduleDayForm(request.POST, prefix='thursday')
        schedule_friday_form = ScheduleDayForm(request.POST, prefix='friday')
        schedule_saturday_form = ScheduleDayForm(request.POST, prefix='saturday')
        schedule_sunday_form = ScheduleDayForm(request.POST, prefix='sunday')
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        if phone_config_form.is_valid():
            PhoneNumberCheckConfig.objects.update_or_create(id=id, defaults={
                'ima_name': phone_config_form.cleaned_data['ima_name'],
                'phone': phone_config_form.cleaned_data['phone'],
                'failure_threshold': phone_config_form.cleaned_data['failure_threshold'],
                'test_frequency': phone_config_form.cleaned_data['test_frequency']
            })
        if schedule_monday_form.is_valid():
            ScheduleDay.objects.update_or_create(phone_config=phone_config, day=ScheduleDay.ScheduleDayType.MONDAY,defaults=schedule_monday_form.cleaned_data)

    context = {
        'phone_config_form': phone_config_form,
        'schedule_monday_form': schedule_monday_form,
        'schedule_tuesday_form': schedule_tuesday_form,
        'schedule_wednesday_form': schedule_wednesday_form,
        'schedule_thursday_form': schedule_thursday_form,
        'schedule_friday_form': schedule_friday_form,
        'schedule_saturday_form': schedule_saturday_form,
        'schedule_sunday_form': schedule_sunday_form

    }

    return render(request, 'pegasus_app/schedule.html', context)


def home_page(request):
    schedule_formset = SchedulesDayFormset(queryset=ScheduleDay.objects.none(),
                                           initial=[{'day': ScheduleDay.ScheduleDayType.MONDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.TUESDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.WEDNESDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.THURSDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.FRIDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.SATURDAY},
                                                    {'day': ScheduleDay.ScheduleDayType.SUNDAY}])
    if request.method == 'POST':
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        schedule_formset = SchedulesDayFormset(request.POST)
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
        'config_form': PhoneNumberCheckConfigForm,
        'schedule_formset': schedule_formset
    }

    return render(request, 'pegasus_app/schedule.html', context)
