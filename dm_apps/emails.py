from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, get_language, activate
from html2text import html2text

from dm_apps import settings
from dm_apps.context_processor import my_envr
from dm_apps.utils import custom_send_mail
from lib.functions.custom_functions import listrify


class Email:
    subject_en = None
    subject_fr = None
    message_en = None
    message_fr = None
    recipient_list = list()
    email_template_path = None
    from_email = settings.SITE_FROM_EMAIL

    def get_subject_en(self):
        return self.subject_en

    def get_subject_fr(self):
        return self.subject_fr

    def get_message_fr(self):
        return self.message_fr

    def get_message_en(self):
        return self.message_en

    def get_email_template_path(self):
        return self.email_template_path

    def get_from_email(self):
        return self.from_email

    def get_recipient_list(self):
        return self.recipient_list

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def __str__(self):
        return f"FROM: {self.get_from_email()}\n" \
               f"TO: {self.get_recipient_list()}\n" \
               f"SUBJECT: {self.get_subject()}\n" \
               f"HTML MESSAGE:\n{html2text(self.get_html_message())}\n" \
               f"PLAIN CONTENT MESSAGE:\n{self.get_text_message()}"

    def as_table(self):
        html = f'<table class="table table-sm table-bordered">' \
               f'<tr><th>{_("From")}</th><td>{self.get_from_email()}</td></tr>' \
               f'<tr><th>{_("To")}</th><td>{listrify(self.get_recipient_list())}</td></tr>' \
               f'<tr><th>{_("Subject")}</th><td>{self.get_subject()}</td></tr>' \
               f'<tr><th>{_("HTML Message Body")}</th><td>{self.get_message()}</td></tr></table>'
        return mark_safe(html)

    def as_dict(self):
        return {
            "from": self.get_from_email(),
            "to": listrify(self.get_recipient_list()),
            "subject": self.get_subject(),
            "message": self.get_message()
        }

    def get_html_message(self):
        t = loader.get_template(self.email_template_path)
        context = self.get_context_data()
        rendered = t.render(context)
        return rendered

    def get_text_message(self):
        message_en = self.get_message_en()
        message_fr = self.get_message_fr()

        if message_en or message_fr:
            if message_en and message_fr:
                msg = f"*** un message français suivra \n\n\n{message_en} " \
                      f"\n\n ******************************************************************** \n\n {message_fr}"
            elif message_en:
                msg = message_en
            else:
                msg = message_fr
            return msg

    def get_message(self):
        """ use this if you only want one message. It will help you decide which one has content """
        text_msg = self.get_text_message()
        html_msg = self.get_html_message()
        # basically, if there is a text message, send in that.
        if text_msg:
            return text_msg
        return html_msg

    def get_subject(self):
        subject_en = self.get_subject_en()
        subject_fr = self.get_subject_fr()

        lang = get_language()
        subject = str()
        if subject_en:
            activate('en')
            subject += subject_en
        if subject_fr:
            if len(subject) > 0:
                subject += " - "
            activate('fr')
            subject += subject_fr
        activate(lang)
        return subject

    def get_context_data(self):
        context = dict()
        if self.instance:
            context["object"] = self.instance
        context.update(my_envr(self.request))
        return context

    def send(self):
        custom_send_mail(
            email_instance=self,
        )
