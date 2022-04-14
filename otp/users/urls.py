from django.urls import path
from users.views import OtpView


urlpatterns = [
    path('otp', OtpView.as_view(), name='otp_view' ),
]
