from mailing.mail_pattenrs.mailjet_builder import MailjetMessageBuilder
from project.settings import sender_email, sender_name


class EmailFactory:
    @staticmethod
    def create(recipient_email, subject, text_part=None, template_name=None, context=None):
        builder = MailjetMessageBuilder()

        # Set sender information
        builder.set_sender(sender_email, sender_name)

        builder.add_recipient(recipient_email)

        builder.set_subject(subject)

        # Set text part (optional)
        if text_part:
            builder.set_text_part(text_part)

        # Set HTML part from template
        if template_name:
            builder.html_part(template_name, context)

        # Add the message to the list of messages
        builder.add_message()

        # Build the data structure containing all the messages
        data = builder.build()

        return data
