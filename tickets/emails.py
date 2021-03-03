from django.conf import settings
from django.contrib.auth.models import User
from django.template import loader

from dm_apps.context_processor import my_envr
from dm_apps.emails import Email

from_email = settings.SITE_FROM_EMAIL
admin_email = 'david.fishman@dfo-mpo.gc.ca'


class NewTicketEmail(Email):
    subject_en = 'A new ticket has been created'
    subject_fr = 'un nouveau billet a été créé'
    email_template_path = 'tickets/email_new_ticket.html'

    def get_recipient_list(self):
        if self.instance.dm_assigned.exists():
            my_to_list = [user.email for user in self.instance.dm_assigned.all()]
        else:
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
        my_to_list.append(self.instance.primary_contact.email)
        return my_to_list


class NewFollowUpEmail(Email):
    subject_en = 'A follow-up has been added to your ticket'
    subject_fr = 'un suivi a été ajouté à votre billet'
    email_template_path = 'tickets/email_follow_up.html'

    def get_recipient_list(self):
        if self.instance.ticket.dm_assigned.exists():
            my_to_list = [user.email for user in self.instance.ticket.dm_assigned.all()]
        else:
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
        my_to_list.append(self.instance.ticket.primary_contact.email)
        return my_to_list


class TicketResolvedEmail(Email):
    subject_en = 'Your ticket has been resolved'
    subject_fr = 'votre billet a été résolu'
    email_template_path = 'tickets/email_ticket_resolved.html'

    def get_recipient_list(self):
        if self.instance.dm_assigned.exists():
            my_to_list = [user.email for user in self.instance.dm_assigned.all()]
        else:
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
        my_to_list.append(self.instance.primary_contact.email)
        return my_to_list

