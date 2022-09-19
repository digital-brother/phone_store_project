from django.contrib import admin

from pegasus_app.models import Phone, Schedule, UserPlan

admin.site.register(Phone)
admin.site.register(Schedule)
admin.site.register(UserPlan)

