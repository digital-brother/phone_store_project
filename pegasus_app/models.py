from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserPlan(models.Model):
    max_phones_numbers = models.IntegerField()
    name = models.CharField(max_length=32)


class PhoneNumberCheckConfig(models.Model):
    ima_name = models.CharField(max_length=64)
    phone = PhoneNumberField()
    failure_threshold = models.IntegerField(validators=[MaxValueValidator(10)])
    test_frequency = models.IntegerField(validators=[MaxValueValidator(120)])
    user_plan = models.ForeignKey('User', on_delete=models.CASCADE)


class ScheduleDay(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    open_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    phone = models.ForeignKey('PhoneNumberCheckConfig', on_delete=models.CASCADE)
