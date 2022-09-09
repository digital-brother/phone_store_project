from django.urls import path

from pegasus_app.views import home_page

urlpatterns = [
    path('', home_page, name='home'),
]