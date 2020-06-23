from django.conf import settings
from django.contrib.auth.models import User
from django.template import loader

from_email = settings.SITE_FROM_EMAIL


class NewEntryEmail:
    def __init__(self, my_object):
        self.subject = 'A new entry has been made in the iHub web app'
        self.message = self.load_html_template(my_object)
        self.from_email = from_email
        self.to_list = [user.email for user in User.objects.filter(groups__in=[18,])]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, my_object):
        t = loader.get_template('ihub/email_new_entry.html')
        field_list = [
            'title',
            'entry_type',
            'organizations',
            'sectors',
            'created_by',
        ]
        context = {'object': my_object, 'field_list': field_list}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered
