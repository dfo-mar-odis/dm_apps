from django.template import loader
from django.conf import settings

from dm_apps.context_processor import my_envr

from_email=settings.SITE_FROM_EMAIL
david_email = 'david.fishman@dfo-mpo.gc.ca'
patrick_email = 'Patrick.Upson@dfo-mpo.gc.ca'

class RequestAccessEmail:

    def __init__(self, context, request):
        self.request = request
        self.subject = '*** Application Access Request - Gulf Science Data Management ***'
        self.message = self.load_html_template(context)
        self.from_email = from_email
        self.to_list = [david_email, patrick_email ]

    def load_html_template(self, context):
        t = loader.get_template('accounts/email_new_access_request.html')
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered
