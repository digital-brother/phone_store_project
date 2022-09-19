from django import forms
from django.forms import inlineformset_factory

from pegasus_app.models import Phone, Schedule


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['ima_name', 'number', 'failure_threshold', 'test_frequency']
        widgets = {
            'ima_name': forms.TextInput(attrs={'label': 'Ima name', 'class': 'form-input'}),
        }


class ScheduleDayForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'is_active', 'open_time', 'close_time']


ScheduleDayFormset = inlineformset_factory(Phone, Schedule, fields='__all__', extra=0, can_delete=False)

