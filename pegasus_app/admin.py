from django.contrib import admin

from pegasus_app.models import PhoneNumberCheckConfig, ScheduleDay, UserPlan

admin.site.register(PhoneNumberCheckConfig)
admin.site.register(ScheduleDay)
admin.site.register(UserPlan)

