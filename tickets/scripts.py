import os

from django.contrib.auth.models import User
from django.core import serializers
from django.core.files import File

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


def export_fixtures():
    """ a simple function to expor the important lookup tables. These fixutre will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    models_to_export = [
        models.Status,
        models.RequestType,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()


