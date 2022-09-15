from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ...


class UserPlan(models.Model):
    max_phones_numbers = models.IntegerField()
    name = models.CharField(max_length=32)

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='plan')

    def __str__(self):
        return self.name


class PhoneNumberCheckConfig(models.Model):
    ima_name = models.CharField(max_length=64)
    phone = PhoneNumberField()
    failure_threshold = models.IntegerField(validators=[MaxValueValidator(10)])
    test_frequency = models.IntegerField(validators=[MaxValueValidator(120)])

    user_plan = models.ForeignKey('UserPlan', on_delete=models.CASCADE, related_name='phone_configs')

    def __str__(self):
        return self.ima_name


class ScheduleDay(models.Model):
    class ScheduleDayType(models.TextChoices):
        MONDAY = 'Monday'
        TUESDAY = 'Tuesday'
        WEDNESDAY = 'Wednesday'
        THURSDAY = 'Thursday'
        FRIDAY = 'Friday'
        SATURDAY = 'Saturday'
        SUNDAY = 'Sunday'

    is_active = models.BooleanField()
    day = models.CharField(max_length=32, choices=ScheduleDayType.choices)
    open_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)

    phone_config = models.ForeignKey('PhoneNumberCheckConfig', on_delete=models.CASCADE, related_name='schedules')
