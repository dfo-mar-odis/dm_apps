from django.conf import settings
from django.template import loader

from dm_apps.context_processor import my_envr

from_email = settings.SITE_FROM_EMAIL



class ProjectApprovalEmail:
    def __init__(self, project, request):
        self.request = request
        if project.approved:
            self.subject = 'Your project has been approved / Votre projet a été approuvé'
        else:
            self.subject = "Your project has not been approved / Votre projet n'a pas été approuvé"

        self.message = self.load_html_template(project)
        self.from_email = from_email
        self.to_list = [u.email for u in project.project_leads_as_users]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, project):
        t = loader.get_template('projects/email_project_approved.html')
        context = {'object': project,}
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered


class ProjectSubmissionEmail:
    def __init__(self, object, request):
        self.request = request
        if object.submitted:
            self.subject = 'A project has been submitted under your section / Un projet a été soumis dans votre section'
        else:
            self.subject = 'A project has been unsubmitted from your section / Un projet a été annulé dans votre section'

        self.message = self.load_html_template(object)
        self.from_email = from_email
        try:
            self.to_list = [object.section.head.email]
        except AttributeError:
            self.to_list = ["david.fishman@dfo-mpo.gc.ca"]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, object):
        t = loader.get_template('projects/email_project_submitted.html')

        project_field_list = [
            'id',
            'project_title',
            'section',
            'project_leads|project_leads',
        ]
        context = {'object': object, 'field_list':project_field_list}
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered



class UserCreationEmail:
    def __init__(self, object, request):
        self.request = request
        self.subject = 'DM Apps account creation / Création de compte DM Apps'
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = []

        try:
            self.to_list.append(object.email)
        except AttributeError:
            self.to_list.append("david.fishman@dfo-mpo.gc.ca")

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, object):
        t = loader.get_template('projects/email_user_creation.html')
        context = {'object': object,}
        context.update(my_envr(self.request))
        rendered = t.render(context)
        return rendered
