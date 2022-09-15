from django.urls import path

from pegasus_app.views import home_page, change_config_number

urlpatterns = [
    path('', home_page, name='home'),
    path('change_config_number/<int:id>', change_config_number, name='change_config_number'),
]