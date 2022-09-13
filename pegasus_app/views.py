from django.shortcuts import render

from pegasus_app.forms import PhoneNumberCheckConfigForm, SchedulesDayFormset
from pegasus_app.models import ScheduleDay


def home_page(request):

    if request.POST:
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        schedules_formset = SchedulesDayFormset(queryset=ScheduleDay.objects.none())
        if phone_config_form.is_valid() and schedules_formset.is_valid():
            phone_config = phone_config_form.save()
            for form in schedules_formset:
                print(form)

        print(request.POST)
    context = {
        'config_form': PhoneNumberCheckConfigForm,
        'schedule_config': SchedulesDayFormset
    }
    return render(request, 'pegasus_app/schedule.html', context)
