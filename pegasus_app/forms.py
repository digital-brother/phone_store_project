from django import forms

from pegasus_app.models import PhoneNumberCheckConfig, ScheduleDay


class PhoneNumberCheckConfigForm(forms.ModelForm):
    class Meta:
        model = PhoneNumberCheckConfig
        fields = ['ima_name', 'phone', 'failure_threshold', 'test_frequency']


SchedulesDayFormset = forms.inlineformset_factory(PhoneNumberCheckConfig, ScheduleDay, fields='__all__', extra=1,
                                                  widgets={
                                                      'day': forms.CheckboxSelectMultiple(attrs={
                                                          'value': 'checkbox',

                                                      }, )
                                                  })
