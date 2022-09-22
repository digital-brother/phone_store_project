from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    @property
    def can_create_phones(self):
        return self.phones.count() < self.plan.max_phones_numbers

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
