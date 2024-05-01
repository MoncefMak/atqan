from django.urls import path
from .views import VerifyOtp

urlpatterns = [
    path('verify-otp/', VerifyOtp.as_view(), name='verify_otp'),
]
