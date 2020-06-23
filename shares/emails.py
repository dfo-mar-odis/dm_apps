from django.conf import settings
from django.template import loader

from_email = settings.SITE_FROM_EMAIL
admin_email = 'david.fishman@dfo-mpo.gc.ca'


class SendInstructionsEmail:
    def __init__(self, object):
        self.subject = 'Your NAS user account has been created'
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = [object.user.email]

    def load_html_template(self, object):
        t = loader.get_template('shares/email_instructions.html')
        context = {'object': object}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered
