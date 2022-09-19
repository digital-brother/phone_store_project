from django.urls import path

from pegasus_app.views import home_page, change_config_number, Phone, PhoneCreateView

urlpatterns = [
    path('', home_page, name='home'),
    path('change_config_number/', change_config_number, name='change_config_number'),
    path('change_config_number/<int:id>', change_config_number, name='change_config_number'),
    path('number/<int:id>/', Phone.as_view(), name='number'),
    path('phones/create/', PhoneCreateView.as_view(), name='phone_create'),
]