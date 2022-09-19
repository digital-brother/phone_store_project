from django.urls import path

from pegasus_app.views import home_page, change_config_number, PhoneView, PhoneCreateView

urlpatterns = [
    path('number/<int:id>/', PhoneView.as_view(), name='number'),
    path('phones/create/', PhoneCreateView.as_view(), name='phone_create'),
]