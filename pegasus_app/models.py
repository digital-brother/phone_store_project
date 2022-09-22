from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
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


class Phone(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='phones')
    ima_name = models.CharField(max_length=64)
    number = PhoneNumberField()
    failure_threshold = models.IntegerField(validators=[MaxValueValidator(10)])
    test_frequency = models.IntegerField(validators=[MaxValueValidator(120)])

    def clean(self):
        count_of_numbers = self.owner.phones.count()
        max_phones_numbers = self.owner.plan.max_phones_numbers

        if count_of_numbers >= max_phones_numbers:
            raise ValidationError(
                "You cannot create a number. Pay attention to your Plan"
            )

    def __str__(self):
        return self.ima_name

    def create_missing_schedules(self):
        for schedule_day_type in Schedule.Day.values:
            schedule_day_obj = self.schedules.filter(day=schedule_day_type).first()
            if not schedule_day_obj:
                Schedule.objects.create(phone=self, day=schedule_day_type)


class Schedule(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'monday'
        TUESDAY = 'tuesday'
        WEDNESDAY = 'wednesday'
        THURSDAY = 'thursday'
        FRIDAY = 'friday'
        SATURDAY = 'saturday'
        SUNDAY = 'sunday'

    is_active = models.BooleanField(null=True)
    day = models.CharField(max_length=32, choices=Day.choices)
    open_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    close_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='schedules', null=True)
