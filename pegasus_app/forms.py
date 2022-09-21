from django import forms
from django.forms import inlineformset_factory

from pegasus_app.models import Phone, Schedule


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['ima_name', 'number', 'failure_threshold', 'test_frequency']
        widgets = {
            'ima_name': forms.TextInput(attrs={'class': 'form-control phone_config-inputs'}),
            'number': forms.TextInput(attrs={'class': 'form-control phone_config-inputs'}),
            'failure_threshold': forms.TextInput(attrs={'type': 'range', 'min': "1", 'max': "10",
                                                        'oninput': 'id_output_failure_threshold.value = id_failure_threshold.value'}),
            'test_frequency': forms.TextInput(attrs={'type': 'range', 'min': '10', 'max': '120', 'step': '5',
                                                     'oninput': 'id_output_test_frequency.value = id_test_frequency.value'})
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'is_active', 'open_time', 'close_time']
        labels = {
            'open_time': 'Open',
            'close_time': 'Close'
        }
        widgets = {
            'is_active': forms.CheckboxInput(),
            'open_time': forms.TextInput(
                attrs={'class': 'schedule_time-input', 'type': 'time'}),
            'close_time': forms.TextInput(
                attrs={'class': 'schedule_time-input', 'type': 'time'})
        }


ScheduleFormset = inlineformset_factory(Phone, Schedule, form=ScheduleForm, extra=7, max_num=7, can_delete=False)
