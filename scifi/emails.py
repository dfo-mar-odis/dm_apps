from django.conf import settings
from django.template import loader

from_email = settings.SITE_FROM_EMAIL
admin_email = 'david.fishman@dfo-mpo.gc.ca'
kim_email = 'Kimberly.Bertolin@dfo-mpo.gc.ca'
yves_email = 'Yves.Despres@dfo-mpo.gc.ca'


class NewEntryEmail:
    def __init__(self, object):
        self.subject = 'A new expense has been entered into SciFi'
        self.message = self.load_html_template(object)
        self.from_email = from_email

        # in order to decide on a "to_list" we have to look at the rc. Anybody attached to the RC should be notified
        if object.responsibility_center.scifi_users.count() > 0:
            self.to_list = [scifi_user.user.email for scifi_user in object.responsibility_center.scifi_users.all()]
        else:
            self.to_list = None

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, object):
        t = loader.get_template('scifi/email_new_entry.html')
        context = {'object': object}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered
