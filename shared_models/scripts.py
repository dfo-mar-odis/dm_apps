import csv
import os
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files import File

from . import models


def resave_sections():
    for s in models.Section.objects.all():
        s.save()

def resave_organizations():
    for obj in models.Organization.objects.all():
        obj.save()


def save_and_add_uuid():
    model_list = [models.Region, models.Branch, models.Division, models.Section, models.Province]

    for model in model_list:
        for obj in model.objects.all():
            if not obj.uuid:
                obj.uuid = uuid.uuid4()
                obj.save()


def pad_codes():
    for port in models.Port.objects.all():
        if len(port.district_code) == 1:
            port.district_code = "0{}".format(port.district_code)
            port.save()
        if len(port.port_code) == 1:
            port.port_code = "0{}".format(port.port_code)
            port.save()


def export_fixtures():
    """ a simple function to expor the important lookup tables. These fixutre will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    models_to_export = [
        models.FiscalYear,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()


def run_import_feb_25_2021():
    foo = ImportFromSpreadsheet("org_list_import_2021_02_24.csv",
                                blank_spots_are_literal=True,
                                create=False,
                                update=True,
                                commit=True
                                )
    foo.digest()


class ImportFromSpreadsheet:
    """
    filename: file name of csv in the shared_models.script_data folder
    blank_spots_are_literal: should blank spots in the spreadsheet be used to indicate a true blank spot in the db?
    commit: should changes to users (head and admin) be committed?
    create: when encoutering an org uuid that is not in db, should it be created?
    update: when a an org is found via uuid, should the name and nom be updated from the data in the spreadsheet?
    """

    def __init__(self, filename, blank_spots_are_literal=True, commit=False, create=True, update=True):
        self.filename = filename
        self.blank_spots_are_literal = blank_spots_are_literal
        self.commit = commit
        self.create = create
        self.update = update

    def digest(self):
        my_target_data_file = os.path.join(settings.BASE_DIR, 'shared_models', 'script_data', self.filename)
        with open(my_target_data_file, 'r') as csv_read_file:
            my_csv = csv.DictReader(csv_read_file)
            for row in my_csv:
                # reset the memory at the top of each row
                region = None
                branch = None
                division = None
                levels = ['region', 'branch', 'division', 'section']
                for level in levels:
                    my_model = getattr(models, level.title())
                    obj = self.__get_create_object_from_uuid(
                        my_model=my_model,
                        uuid=row[f"{level} uuid"],
                        name=row[f"{level} name"],
                        nom=row[f"{level} nom"],
                    )
                    if obj:
                        # head
                        self.__db_user_to_spreadsheet(
                            obj=obj,
                            target_email=row[f"{level} head email"],
                            user_type="head",
                        )
                        # admin
                        self.__db_user_to_spreadsheet(
                            obj=obj,
                            target_email=row[f"{level} admin email"],
                            user_type="admin",
                        )

                        # set memory and make sure org objects are linked appropriately
                        if level == 'region':
                            region = obj
                        elif level == 'branch':
                            branch = obj
                            if obj.region != region:
                                print(f'*** Updating Region for Branch {obj}: {obj.region} to {region}')
                                if self.commit:
                                    obj.region = region
                                    obj.save()
                        elif level == 'division':
                            division = obj
                            if obj.branch != branch:
                                print(f'*** Updating Branch for Division {obj}: {obj.branch} to {branch}')
                                if self.commit:
                                    obj.branch = branch
                                    obj.save()
                        elif level == 'section':
                            if obj.division != division:
                                print(f'*** Updating Division for Section {obj}: {obj.division} to {division}')
                                if self.commit:
                                    obj.division = division
                                    obj.save()

    def __db_user_to_spreadsheet(self, obj, target_email, user_type):
        db_user = getattr(obj, user_type)  # e.g. region.head
        # if there is no email and we are meant to take this literally, we should clear the user in db table, if any
        faked_msg = "  **FAKED**" if not self.commit else ""
        if not target_email:  # doing this in two steps do create a deadend
            if self.blank_spots_are_literal and db_user:
                print(f"clearing user {db_user} ({user_type.upper()}) from {obj}." + faked_msg)
                setattr(obj, user_type, None)
            elif db_user:
                print(f"no email for {obj} listed on spreadsheet, but not taking action since blank spots are not to be taken literally. {db_user} is spared.")
            else:
                # then there is no action to take :)
                pass
        # there is an email from spreadsheet
        else:
            qs = User.objects.filter(email__iexact=target_email)
            # the user's email DOES NOT exists in the db
            if not qs.exists():
                first_name = target_email.split("@")[0].split(".")[0].title()
                last_name = target_email.split("@")[0].split(".")[1].title()
                target_user = User.objects.create(first_name=first_name, last_name=last_name, email=target_email, username=target_email, is_active=True)
                print(f'new user created: {target_user}')
            else:
                target_user = qs.first()

            # now that we have a user, we can make our final assessment in one go:
            if target_user != db_user:
                print(f"{target_user} is replacing {db_user} in {obj}." + faked_msg)
                setattr(obj, user_type, target_user)

        if self.commit:
            obj.save()

    def __get_create_object_from_uuid(self, my_model, uuid, name, nom):
        faked_msg = "  **FAKED**" if self.commit else ""
        qs = my_model.objects.filter(uuid=uuid)
        if qs.exists():
            obj = qs.first()
            if self.update:
                if obj.name != name or obj.nom != nom:
                    print(f'{my_model._meta.verbose_name} {obj.name} is being updated.' + faked_msg)
                    obj.name = name
                    obj.nom = nom

                    if self.commit:
                        obj.save()

            return obj
        else:
            if self.create:
                obj = my_model.objects.create(uuid=uuid, name=name, nom=nom)
                print(f'{my_model._meta.verbose_name} called {obj} was created')
                return obj
            else:
                print(f'{my_model._meta.verbose_name} with uuid {uuid} NOT found: name = {name} / nom = {nom}')


def test_email():
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name="ca-central-1")
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': ["david.fishman@dfo-mpo.gc.ca"]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': "test",
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': "test",
                },
            },
            Source=settings.SITE_FROM_EMAIL,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])