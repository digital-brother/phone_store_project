from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView

from pegasus_app.forms import PhoneNumberCheckConfigForm, SchedulesDayFormset
from pegasus_app.models import ScheduleDay, PhoneNumberCheckConfig


def change_config_number(request, id):
    phone_config = PhoneNumberCheckConfig.objects.get(id=id)
    if request.method == 'POST':
        phone_config_form = PhoneNumberCheckConfigForm(request.POST or None, instance=phone_config)
        schedule_formset = SchedulesDayFormset(request.POST or None, instance=phone_config)
        if phone_config_form.is_valid():
            phone_config = phone_config_form.save(commit=False)
            phone_config.user_plan = request.user.plan
            phone_config.save()
            for form in schedule_formset:
                if form.is_valid() and len(form.cleaned_data):
                    form.cleaned_data['phone_config'] = phone_config
                    form.save()

    context = {
        'config_form': PhoneNumberCheckConfigForm(instance=phone_config),
        'schedule_formset': SchedulesDayFormset(instance=phone_config)

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
