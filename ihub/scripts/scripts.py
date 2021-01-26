import csv
import datetime
import os

from django.conf import settings
from django.core import serializers
from django.core.files import File
from django.urls import reverse

from ihub import models
from lib.templatetags.custom_filters import nz
from masterlist import models as ml_models
from shared_models import models as shared_models


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
    for contact in ml_models.Person.objects.all():
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


def digest_qc_data():
    # open the csv we want to read
    my_target_data_file = os.path.join(settings.BASE_DIR, 'ihub', 'quebec_data.csv')
    with open(my_target_data_file, 'r') as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)

        # stuff that has to happen for running the loop
        qc_region = shared_models.Region.objects.get(name="Quebec")
        models.Status.objects.get_or_create(name="cancelled")  # make sure the cancelled status exists

        for row in my_csv:

            # title
            entry, created = models.Entry.objects.get_or_create(
                title=row["title"],
            )
            if created:
                entry.old_id = entry.id
                entry.save()
            entry.regions.add(qc_region)

            # Org...
            try: org = ml_models.Organization.objects.get(name__icontains=row["org"])
            except:
                org = None
                if row["org"] and row["org"] != "":
                    org = ml_models.Organization.objects.create(name=row["org"])
                    print(f"Creating new organization: {org.name} ({org.id}) --> {reverse('ihub:org_detail', args=[org.id])}")
                    entry.organizations.add(org)

            # Sector
            sector, created = ml_models.Sector.objects.get_or_create(
                name=row["sector"],
                region=qc_region,
            )
            entry.sectors.add(sector)

            # type
            try: type = models.EntryType.objects.get(name__iexact=row["type"])
            except:
                type = None
                if row["type"] == 'Mobilisation':
                    type = models.EntryType.objects.get(name__iexact="engagement")
                else:
                    print("can't find: ", row["type"])
            entry.entry_type = type


            # status
            try: status = models.Status.objects.get(name__icontains=row["status"])
            except: print("can't find: ", row["status"])

            entry.status = status

            # date1
            dt=None
            date1 = nz(row["date1"],None)
            if date1:
                if len(date1.split("/")) == 3:
                    dt = datetime.datetime.strptime(date1, "%m/%d/%Y")
                    entry.initial_date = dt
                else:
                    print(f'Cannot parse start date for Entry #{entry.id}: {date1}')
            else:
                print(f'No start date in spreadsheet for Entry #{entry.id}: {date1}')

            # date2
            dt=None
            date2 = nz(row["date2"], None)
            if date1:
                if len(date2.split("/")) == 3:
                    dt = datetime.datetime.strptime(date2, "%m/%d/%Y")
                    entry.initial_date = dt
                else: print(f'Cannot parse start date for Entry #{entry.id}: {date2}')
            else: print(f'No start date in spreadsheet for Entry #{entry.id}: {date2}')

            entry.save()


            # contact
            person, created = models.EntryPerson.objects.get_or_create(
                entry=entry,

            )




def delete_all_data():
    models.Entry.objects.filter(old_id__isnull=False).delete()
