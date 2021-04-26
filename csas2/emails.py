from django.utils.translation import gettext as _

from dm_apps.emails import Email


class InvitationEmail(Email):
    email_template_path = 'csas2/emails/invitation.html'
    subject_en = 'You have been invited to attend an event! (*** ACTION REQUIRED ***)'
    subject_fr = "Vous avez été invité à assister à un événement! (*** ACTION REQUISE ***)"

    def get_recipient_list(self):
        return [self.instance.person.email]

    def get_context_data(self):
        context = super().get_context_data()
        field_list = [
            'process',
            'type',
            'location',
            'display_dates|{}'.format(_("dates")),
        ]
        context.update({'event': self.instance, 'field_list': field_list})
        return context


class NewResourceEmail(Email):
    email_template_path = 'csas2/emails/new_resource.html'
    subject_en = 'A new resource is available'
    subject_fr = "Une nouvelle ressource est disponible"

    def get_recipient_list(self):
        return [self.instance.person.email]

    def get_context_data(self):
        context = super().get_context_data()
        field_list = [
            'process',
            'type',
            'location',
            'display_dates|{}'.format(_("dates")),
        ]
        context.update({'object': self.instance, 'resource': self.resource, 'field_list': field_list})
        return context

    def __init__(self, request, instance=None, resource=None):
        super().__init__(request)
        self.request = request
        self.instance = instance
        self.resource = resource