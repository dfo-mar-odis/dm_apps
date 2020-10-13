import csv
import os

from django.core import serializers
from django.core.files import File

from ihub import models
from shared_models import models as shared_models
from masterlist import models as ml_models

def export_fixtures():
    """ a simple function to expor the important lookup tables. These fixutre will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fixtures')
    models_to_export = [
        models.EntryType,
        models.Status,
        models.FundingPurpose,
        models.FundingProgram,
        ml_models.Nation,
        ml_models.RelationshipRating,
        ml_models.Grouping,
        shared_models.FiscalYear,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()



def clean_masterlist():
    for contact in ml_models.Person.objects.filter(ihub_vetted=False):
        if not contact.project_people.count():
            try:
                contact.delete()
            except:
                print("cannot delete contact")

    for org in ml_models.Organization.objects.all():
        if not org.members.count() and not org.entries.count() and not org.projects.count():
            try:
                org.delete()
            except:
                print("cannot delete org")
