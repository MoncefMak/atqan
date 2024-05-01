from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from accounts.utils import generate_otp
from mailing.tasks import send_email_task
from otp.models import Otp
from project.settings import TEST_CASE


@receiver(post_save, sender=User)
def send_otp(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        otp = Otp.objects.create(user=instance, otp_code=generate_otp())
        if not TEST_CASE:
            subject = 'One-Time Password (OTP) Email'
            send_email_task.delay(recipient_email=instance.email,
                                  subject=subject,
                                  template_name='otp_template',
                                  context={'email': instance.email, 'otp': otp.otp_code})
