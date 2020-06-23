from django.conf import settings
from django.contrib.auth.models import User
from django.template import loader

from_email = settings.SITE_FROM_EMAIL
admin_email = 'david.fishman@dfo-mpo.gc.ca'


class NewTicketEmail:
    def __init__(self, ticket_object):
        self.subject = 'A new ticket has been created / un nouveau billet a été créé'
        self.message = self.load_html_template(ticket_object)
        self.from_email = from_email

        # decide on who should receive the email
        if ticket_object.dm_assigned.count() > 0:
            my_to_list = [user.email for user in ticket_object.dm_assigned.all()]
            my_to_list.append(ticket_object.primary_contact.email)
        else:
            # get a list of all staff email addresses
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
            my_to_list.append(ticket_object.primary_contact.email)
        self.to_list = my_to_list

    def load_html_template(self, ticket_object):
        t = loader.get_template('tickets/email_new_ticket.html')
        context = {'object': ticket_object}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)



class NewFollowUpEmail:
    def __init__(self, object):
        self.subject = 'A follow-up has been added to your ticket / un suivi a été ajouté à votre billet'
        self.message = self.load_html_template(object)
        self.from_email = from_email

        # decide on who should receive the email
        if object.ticket.dm_assigned.count() > 0:
            my_to_list = [user.email for user in object.ticket.dm_assigned.all()]
            my_to_list.append(object.ticket.primary_contact.email)
        else:
            # get a list of all staff email addresses
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
            my_to_list.append(object.ticket.primary_contact.email)
        self.to_list = my_to_list

    def load_html_template(self, object):
        t = loader.get_template('tickets/email_follow_up.html')
        context = {'object': object}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)



class NewFileAddedEmail:
    def __init__(self, object):
        self.subject = "A new file has been added to Ticket #{}".format(object.ticket.id)
        self.message = self.load_html_template(object)
        self.from_email = from_email
        if object.ticket.dm_assigned.count() > 0:
            my_to_list = [user.email for user in object.ticket.dm_assigned.all()]
            my_to_list.append(object.ticket.primary_contact.email)
        else:
            # get a list of all staff email addresses
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
            my_to_list.append(object.ticket.primary_contact.email)
        self.to_list = my_to_list

    def load_html_template(self, object):
        t = loader.get_template('tickets/email_new_file.html')
        context = {'object': object}
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)


class TicketResolvedEmail:
    def __init__(self, ticket_object):
        self.ticket_object = ticket_object
        self.subject = 'Your ticket has been resolved / votre billet a été résolu'
        self.message = self.load_html_template()
        self.from_email = from_email
        # decide on who should receive the email
        if ticket_object.dm_assigned.count() > 0:
            my_to_list = [user.email for user in ticket_object.dm_assigned.all()]
            my_to_list.append(ticket_object.primary_contact.email)
        else:
            # get a list of all staff email addresses
            my_to_list = [user.email for user in User.objects.filter(is_staff=True)]
            my_to_list.append(ticket_object.primary_contact.email)
        self.to_list = my_to_list


    def load_html_template(self):
        t = loader.get_template('tickets/email_ticket_resolved.html')
        context = {
            'object': self.ticket_object,
        }
        context.update({"SITE_FULL_URL": settings.SITE_FULL_URL})
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)
