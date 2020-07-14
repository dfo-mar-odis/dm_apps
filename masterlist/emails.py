from django.conf import settings
from django.template import loader

from dm_apps.context_processor import my_envr

from_email = settings.SITE_FROM_EMAIL
admin_email = 'david.fishman@dfo-mpo.gc.ca'
stacy_email = 'Stacy.Adeogba@dfo-mpo.gc.ca'


class NewEntryEmail:
    def __init__(self, object, request):
        self.request = request
        self.subject = 'a new entry has been made in the iHub web app'
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = [stacy_email]

    def load_html_template(self, object):
        t = loader.get_template('ihub/email_new_entry.html')
        context = {'object': object}
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered
