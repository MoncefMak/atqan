# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OtpVerificationSerializer
from drf_spectacular.utils import extend_schema


class VerifyOtp(APIView):
    @extend_schema(
        request=OtpVerificationSerializer,
        responses={status.HTTP_200_OK: {"description": "User activated successfully"}},
        auth=[]
    )
    def post(self, request):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp_code']
            user = otp.user
            user.is_active = True
            user.save()
            otp.is_active = False
            otp.save()
            return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
