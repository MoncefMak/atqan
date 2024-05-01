from rest_framework import serializers
from .models import Otp


class OtpVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, value):
        otp = Otp.objects.filter(otp_code=value, is_active=True).first()
        if not otp:
            raise serializers.ValidationError("Invalid OTP or OTP expired")
        return otp
