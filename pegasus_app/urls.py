from django.urls import path

from pegasus_app.views import PhoneCreateView, PhoneEditView

urlpatterns = [
    path('phones/<int:phone_id>/', PhoneEditView.as_view(), name='phone_edit'),
    path('phones/create/', PhoneCreateView.as_view(), name='phone_create'),
]
