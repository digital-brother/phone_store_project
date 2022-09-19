from django.urls import path

from pegasus_app.views import PhoneView

urlpatterns = [
    path('phones/<int:phone_id>/', PhoneView.as_view(), name='phone_edit'),
    path('phones/create/', PhoneView.as_view(), name='phone_create'),
]