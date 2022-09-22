from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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

    def clean(self):
        if not self.owner.can_create_phones:
            max_phone_numbers = self.owner.plan.max_phones_numbers
            raise ValidationError(f'User cannot create more than {max_phone_numbers} phones according to his plan.')

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
