from django.conf import settings
from django.contrib.auth.models import User
from django.template import loader

from dm_apps.context_processor import my_envr

from_email = settings.SITE_FROM_EMAIL
admin_email = 'elizabeth.thompson@dfo-mpo.gc.ca'


class NewIncidentEmail:
    def __init__(self, incident_object, request):
        self.request = request
        self.subject = 'A new incident has been logged / un nouveau incident a été enregistré'
        self.message = self.load_html_template(incident_object)
        self.from_email = from_email
        self.to_list = ["WhaleSightings.XMAR@dfo-mpo.gc.ca",
                        "DFO.GLFWhales-BaleinesGLF.MPO@dfo-mpo.gc.ca"
                        ]

    def load_html_template(self, incident_object):
        t = loader.get_template('whalebrary/email_incident.html')
        context = {'object': incident_object}
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject,
                                                                  self.message)
