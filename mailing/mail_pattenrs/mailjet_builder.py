from django.template import loader


class MailjetMessageBuilder:
    def __init__(self):
        self.data = {
            'Messages': []
        }
        self.current_message = {}

    def set_sender(self, sender_email, sender_name="Me"):
        self.current_message["From"] = {"Email": sender_email, "Name": sender_name}

    def add_recipient(self, recipient_email, recipient_name="You"):
        recipient = {"Email": recipient_email, "Name": recipient_name}
        if "To" not in self.current_message:
            self.current_message["To"] = []
        self.current_message["To"].append(recipient)

    def set_subject(self, subject):
        self.current_message["Subject"] = subject

    def set_text_part(self, text_part):
        self.current_message["TextPart"] = text_part

    def html_part(self, template_name, context=None):
        template_path = f"{template_name}.html"
        template = loader.get_template(template_path)
        context_dict = context if isinstance(context, dict) else {}
        html_content = template.render(context_dict)
        self.current_message['HTMLPart'] = html_content

    def add_message(self):
        self.data['Messages'].append(self.current_message)
        self.current_message = {}

    def build(self):
        return self.data
