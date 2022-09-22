from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import inlineformset_factory

from pegasus_app.models import Phone, Schedule


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['ima_name', 'number', 'failure_threshold', 'test_frequency', 'owner']
        widgets = {
            'ima_name': forms.TextInput(attrs={'class': 'form-control phone_config-inputs'}),
            'number': forms.TextInput(attrs={'class': 'form-control phone_config-inputs'}),
            'failure_threshold': forms.TextInput(attrs={'type': 'range', 'min': "1", 'max': "10",
                                                        'oninput': 'id_output_failure_threshold.value = id_failure_threshold.value'}),
            'test_frequency': forms.TextInput(attrs={'type': 'range', 'min': '10', 'max': '120', 'step': '5',
                                                     'oninput': 'id_output_test_frequency.value = id_test_frequency.value'})
        }

    # def __init__(self, request, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(PhoneForm, self).__init__(*args, **kwargs)
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     user = self.request.user
    #     print(user)
    #     return cleaned_data


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

    def clean(self):
        # import ipdb; ipdb.set_trace()
        is_active = self.cleaned_data.get('is_active', False)
        if is_active:
            # validate the activity name
            open_time = self.cleaned_data.get('open_time', None)
            close_time = self.cleaned_data.get('close_time', None)
            if open_time in EMPTY_VALUES:
                self._errors['open_time'] = self.error_class([
                    'Open time required here'])
            else:
                self.cleaned_data['open_time']
            if close_time in EMPTY_VALUES:
                self._errors['close_time'] = self.error_class([
                    'Close time required here'])
            else:
                self.cleaned_data['close_time']

        return self.cleaned_data


ScheduleFormset = inlineformset_factory(Phone, Schedule, form=ScheduleForm, extra=7, max_num=7, can_delete=False)
