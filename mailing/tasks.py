from celery import shared_task
from mailjet_rest import Client

from mailing.mail_pattenrs.email_factory import EmailFactory
from project.settings import api_key, api_secret


@shared_task
def send_email_task(recipient_email, subject, template_name, text_part=None, context=None):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    email_data = EmailFactory.create(
        recipient_email=recipient_email,
        subject=subject,
        text_part=text_part,
        template_name=template_name,
        context=context
    )
    mailjet.send.create(data=email_data)
