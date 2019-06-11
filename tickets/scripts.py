from django.contrib.auth.models import User

from . import models


def resave_all_tickets(tickets=models.Ticket.objects.all()):
    for t in tickets:
        t.save()


def resave_all_tickets2(tickets=models.Ticket.objects.all()):
    for t in tickets:
        if t.people.count() > 1:
            t.people_notes = ""
            for p in t.people.all():
                t.people_notes += "{} (email={}, phone={}, notes={}); ".format(p.full_name, p.email, p.phone, p.notes)

            t.save()
