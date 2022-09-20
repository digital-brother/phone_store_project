from django import forms
from django.forms import inlineformset_factory

from pegasus_app.models import Phone, Schedule


class PhoneForm(forms.ModelForm):
    ima_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin-bottom: 20px;'}))
    number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin-bottom: 20px;'}))
    failure_threshold = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'range', 'min': "1", 'max': "10",
                                                                         'oninput': 'id_output_failure_threshold.value = id_failure_threshold.value'}))
    test_frequency = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'range', 'min': '10', 'max': '120', 'step': '5',
                                      'oninput': 'id_output_test_frequency.value = id_test_frequency.value'}))

    class Meta:
        model = Phone
        fields = ['ima_name', 'number', 'failure_threshold', 'test_frequency']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'is_active', 'open_time', 'close_time']


ScheduleFormset = inlineformset_factory(Phone, Schedule, form=ScheduleForm, extra=7, max_num=7, can_delete=False)
