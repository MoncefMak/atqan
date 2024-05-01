# import secrets
# default=secrets.token_hex(3)


from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['is_active', 'otp_code'], name='unique_active_otp')
        ]