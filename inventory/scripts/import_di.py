import csv
import datetime
import http.client
import os
import uuid
import xml.etree.ElementTree as ET

import requests
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import make_aware
from inventory import models
from django.conf import settings

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from inventory import xml_export


def get_create_user(email):
    try:
        my_user = User.objects.get(email__iexact=email)
    except User.MultipleObjectsReturned:
        print(email)
    except User.DoesNotExist:
        # if it is a DFO email, then it should be easy..
        email = email.lower()
        names = email.split("@")[0].split(".")
        first_name = names[0]
        last_name = names[-1]
        # print(email, first_name, last_name, names)

        # if this is a dfo email, and there is a first and last name, they can be set as an active user
        if "dfo" in email and len(names) > 1:
            is_active = True
        else:
            is_active = False

        my_user = User.objects.create(
            username=email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
            is_active=is_active,
            email=email,
        )
        print("new user created:", my_user.first_name, my_user.last_name, my_user.email, "is_active=", is_active)
    finally:
        return my_user


def restart():
    models.Resource.objects.filter(section_id=61).delete()


target_dir = os.path.join(settings.BASE_DIR, 'inventory', 'temp')


def import_paas():
    with open(os.path.join(target_dir, "paa.csv"), 'r', encoding="utf8") as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)
        for row in my_csv:
            item, created = shared_models.PAAItem.objects.get_or_create(
                code=row["\ufeffcode"],
                # name=row["english"],
                # nom=row["french"],
            )
            item.name = row["english"]
            item.nom = row["french"]
            item.save()


"""﻿
ID --> this will be a new field
ODIP --> redundant
On OGP --> redundant with url
Dataset title English: --> good.
Dataset title French: --> good
Dataset description English: --> good
Dataset description French: --> good
Your name: --> nix
Your title/role: --> nix
Data owner's name: --> owner
Data owner's email: --> owner email
Data owner's sector: --> this will be tricky. Maybe we can create a generic section from each region based on this set. 
Data owner's Directorate/Branch/Division: --> 
Data owner's region: --> 
IT custodian's name:  --> messy.
Date: --> what is this date?
Source/location of dataset:  --> sometimes a url, othertimes a location on a drive or in a building
Is the dataset publicly available? --> 
Location (if yes): --> These can be concatinated to open data notes
Location (French): --> 
Corresponding Pub/Bib Record --> This can be appended to notes section but should be prefaced by: "needs to be properly added as a citation in the record"
Do you have a data quality process in place? --> appended to notes
Is/can the dataset be machine readable and platform independent? --> appended to notes
What is the current format of the source dataset? --> needs to be parse by data_distribution_formats.py
What is the estimated volume of the dataset (in GB)? --> notes
What is the geographic coverage of the dataset? --> geo_descr_eng
Other, please describe: --> we can do a search here for bounding box. Otherwise can be appended to notes
Is the data for this dataset derived from more than one source? --> notes
How often does the source data change? --> maintenance frequency…problem is split between two cols. If we concatenate then search for FK. If not found, append as note.
If "Other", please indicate time frame: --> 
What is the date range of the dataset? --> needs to be digested. Very problematic though because of the use of hyphen
How does the dataset link to DFO's Program Alignment Architecture (PAA)? --> need to create a new FK
NOTES --> append to notes; may contain an FGP url…
Canada.ca pages where dataset is used --> append to open data  notes
ODIP - Date Pub --> unsure
Spatial/Non-Spatial --> new field needed
Review Dec 2018 --> append to notes
Openess Rating --> append to notes
"""


def import_file():
    with open(os.path.join(target_dir, "annette_open_data.csv"), 'r', encoding="utf8") as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)
        i = 0
        existing_records = 0
        for row in my_csv:
            # only start on row #2
            if i >= 1:

                # most important thing is to establish a uuid. I have verified that the On OGP field is a reliable way to get the uuid
                # i also verified that the best field to get the url / uuid would be row["Location (if yes):"]

                uuid_found = "https://open.canada.ca" in row["Location (if yes):"]

                if uuid_found:
                    uuid = row["Location (if yes):"].split("/")[-1]
                    # we will use the uuid as the basis for grabbing / creating a record
                    if models.Resource.objects.filter(uuid=uuid).count() > 1:
                        r, created = models.Resource.objects.get_or_create(uuid=uuid, notes="WARNING: Duplicate uuid in system.")
                    else:
                        r, created = models.Resource.objects.get_or_create(uuid=uuid)
                    if not created:
                        print("found matching uuid")
                        existing_records += 1

                # otherwise, using the odi_id is not a bad idea.
                else:

                    if models.Resource.objects.filter(title_eng__iexact=row["Dataset title English:"]).count() > 1:
                        r = models.Resource.objects.filter(title_eng__iexact=row["Dataset title English:"]).first()
                    else:
                        r, created = models.Resource.objects.get_or_create(title_eng__iexact=row["Dataset title English:"])
                    if not created:
                        print("found matching title")
                        existing_records += 1

                r.odi_id = row["\ufeffID"]

                # ok, now we have our full dataset nucleated in the db
                # let's tackle each row.

                # Dataset title English: --> good.
                # Dataset title French: --> good
                # Dataset description English: --> good
                # Dataset description French: --> good
                if created:
                    r.title_eng = row["Dataset title English:"]
                    r.title_fre = row["Dataset title French:"]
                    r.descr_eng = row["Dataset description English:"]
                    r.descr_fre = row["Dataset description French:"]

                # add the data owner
                # Data owner's name: --> owner
                # Data owner's email: --> owner email

                # if the email address is missing, means there is no custodian. Let's add annette for interim
                if "@" not in row["Data owner's email:"]:
                    my_user = get_create_user("Annette.Anthony@dfo-mpo.gc.ca")
                    my_role = models.PersonRole.objects.get(id=1)  # steward
                    print("there was no email, so adding annette instead.")
                else:
                    raw = row["Data owner's email:"].replace(" ", "").replace("\n", "")
                    # we will have to clean up the email address(es)
                    if "," in raw or ";" in raw:
                        if "," in raw:
                            emails = raw.split(",")
                        else:
                            emails = raw.split(";")
                    else:
                        emails = [raw, ]

                    # let's cycle through the emails
                    for email in emails:
                        if "@" in email:
                            my_user = get_create_user(email)
                            my_role = models.PersonRole.objects.get(id=1)  # owner
                            models.Person.objects.get_or_create(user=my_user)
                            models.ResourcePerson.objects.get_or_create(
                                resource=r,
                                person_id=my_user.id,
                                role=my_role
                            )

                if r.notes:
                    r.notes += "\n\n"
                else:
                    r.notes = ""  # to prime the field

                if r.open_data_notes:
                    r.open_data_notes += "\n\n"
                else:
                    r.open_data_notes = ""  # to prime the field

                if not "This record has been automatically imported" in r.notes:
                    r.notes += f'{timezone.now().strftime("%B %d, %Y")}: This record has been automatically imported into DM Apps from the Open Data Inventory. These notes will have to be cleaned up.'
                    r.notes += '-------------------------------------------------------------'

                # What is the date range of the dataset? --> needs to be digested. Very problematic though because of the use of hyphen
                field = "What is the date range of the dataset?"
                if not field in r.notes:
                    r.notes += "\n{} {}".format(field, row[field])

                # since the governance will not line up, let's just add this to notes
                # Data owner's region: -->
                # Data owner's sector: --> this will be tricky. Maybe we can create a generic section from each region based on this set.
                # Data owner's Directorate/Branch/Division: -->
                if not "Data owner's region" in r.notes:
                    r.notes += "\nData owner's region: {}".format(row["Data owner's region:"])
                    r.notes += "\nData owner's sector: {}".format(row["Data owner's sector:"])
                    r.notes += "\nData owner's Directorate/Branch/Division: {}".format(row["Data owner's Directorate/Branch/Division:"])

                # IT custodian's name:  --> messy.
                field = "IT custodian's name: "
                r.notes += "\n{} {}".format(field, row[field])

                # Date: --> what is this date?

                # Source/location of dataset:  --> need to parse this out and extract the uuid.
                if uuid_found and not r.public_url:
                    r.public_url = row["Source/location of dataset: "]
                else:
                    field = "Source/location of dataset: "
                    if not field in r.open_data_notes:
                        r.open_data_notes += "\n{} {}".format(field, row[field])

                # Location (if yes): --> These can be concatinated to open data notes
                field = "Location (if yes):"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # Location (French): -->
                field = "Location (French):"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # Corresponding Pub/Bib Record --> This can be appended to notes section but should be prefaced by: "needs to be properly added as a citation in the record"
                field = "Corresponding Pub/Bib Record"
                if not field in r.open_data_notes:
                    r.notes += "\n{}: {}".format(field, row[field])

                # Do you have a data quality process in place? --> appended to notes
                if not r.qc_process_descr_eng:
                    r.qc_process_descr_eng = "Do you have a data quality process in place? {}".format(
                        row["Do you have a data quality process in place?"])

                # Is/can the dataset be machine readable and platform independent? --> appended to notes
                field = "Is/can the dataset be machine readable and platform independent?"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # What is the current format of the source dataset? --> needs to be parse by data_distribution_formats.py
                field = "What is the current format of the source dataset?"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # What is the estimated volume of the dataset (in GB)? --> notes
                field = "What is the estimated volume of the dataset (in GB)?"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # What is the geographic coverage of the dataset? --> geo_descr_eng
                # Other, please describe: --> we can do a search here for bounding box. Otherwise can be appended to notes
                field = "What is the geographic coverage of the dataset?"
                field1 = "Other, please describe:"
                if not r.geo_descr_eng:
                    r.geo_descr_eng = "\n{} {}; {}".format(field, row[field], row[field1])

                # Is the data for this dataset derived from more than one source? --> notes
                field = "Is the data for this dataset derived from more than one source?"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # How often does the source data change? --> maintenance frequency…problem is split between two cols. If we concatenate then search for FK. If not found, append as note.
                # If "Other", please indicate time frame: -->
                field = "How often does the source data change?"
                field1 = 'If "Other", please indicate time frame:'
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}; {}".format(field, row[field], row[field1])

                # NOTES --> append to notes; may contain an FGP url…
                field = "NOTES"
                if not field in r.notes:
                    r.notes += "\n{} {}".format(field, row[field])

                # Canada.ca pages where dataset is used --> append to open data  notes
                field = "Canada.ca pages where dataset is used"
                if not field in r.notes:
                    r.notes += "\n{} {}".format(field, row[field])

                # ODIP - Date Pub --> unsure
                field = "ODIP - Date Pub"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # Spatial/Non-Spatial --> new field needed
                field = "Spatial/Non-Spatial"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{} {}".format(field, row[field])

                # Review Dec 2018 --> append to notes
                field = "Review Dec 2018"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{}: {}".format(field, row[field])

                # Openess Rating --> append to notes
                field = "Openess Rating"
                if not field in r.open_data_notes:
                    r.open_data_notes += "\n{}: {}".format(field, row[field])

                r.save()
                xml_export.verify(r)
                # How does the dataset link to DFO's Program Alignment Architecture (PAA)? --> need to create a new FK
                field = "How does the dataset link to DFO's Program Alignment Architecture (PAA)?"
                list1 = row[field].replace(";", ",").split(",")
                paa_code_list = [paa.code for paa in shared_models.PAAItem.objects.all()]
                for paa in list1:
                    my_code = paa.lstrip().split(" ")[0]
                    if my_code in paa_code_list:
                        r.paa_items.add(shared_models.PAAItem.objects.get(code=my_code))

            i += 1

    print(f"there were {existing_records} records already in the system")
    print(f"there were a total of {i} records processed")


def get_custodians():
    with open(os.path.join(target_dir, "annette_open_data.csv"), 'r', encoding="utf8") as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)
        i = 0
        matches = 0
        non_matches = 0
        for row in my_csv:
            # only start on row #2
            if i >= 1:

                # most important thing is to establish a uuid. I have verified that the On OGP field is a reliable way to get the uuid
                # i also verified that the best field to get the url / uuid would be row["Location (if yes):"]

                r = models.Resource.objects.get(odi_id=row["\ufeffID"])

                # see if we can make a connection with the data custodian from annette's list
                raw_name = row["Your name:"]
                # print(raw_name)

                # if there is a comma, there are two people involved.
                custodians = raw_name.split(",")

                for c in custodians:
                    # there is one name that is a generic inbox. this should be excluded.
                    if "DFO" not in c and len(c.split(" ")) > 1:
                        # lets see if we can find a match
                        first_name = c.split(" ")[0].lstrip().replace("é", "e").replace("É", "E").replace("è", "e").replace("î",
                                                                                                                            "i").lower()
                        last_name = c.split(" ")[1].lstrip().replace("é", "e").replace("É", "E").replace("è", "e").replace("î", "i").lower()
                        qs = User.objects.filter(
                            first_name__icontains=first_name,
                            last_name__icontains=last_name
                        )
                        if qs.count() == 1:
                            matches += 1

                            my_user = User.objects.get(
                                first_name__icontains=first_name,
                                last_name__icontains=last_name
                            )
                            my_role = models.PersonRole.objects.get(id=1)  # owner
                            models.Person.objects.get_or_create(user=my_user)
                            models.ResourcePerson.objects.get_or_create(
                                resource=r,
                                person_id=my_user.id,
                                role=my_role
                            )

                        else:
                            non_matches += 1
                            email = f'{first_name}.{last_name}@dfo-mpo.gc.ca'
                            my_user = get_create_user(email)
                            my_role = models.PersonRole.objects.get(id=1)  # owner
                            models.Person.objects.get_or_create(user=my_user)
                            models.ResourcePerson.objects.get_or_create(
                                resource=r,
                                person_id=my_user.id,
                                role=my_role
                            )
                        print(f"Adding {first_name} {last_name} as custodian to {r}.")
            i += 1


def attach_paa():
    with open(os.path.join(target_dir, "annette_open_data.csv"), 'r', encoding="utf8") as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)
        i = 0
        existing_records = 0

        for row in my_csv:
            # only start on row #2
            if i >= 1:

                # most important thing is to establish a uuid. I have verified that the On OGP field is a reliable way to get the uuid
                # i also verified that the best field to get the url / uuid would be row["Location (if yes):"]

                r = models.Resource.objects.get(odi_id=row["\ufeffID"])

                field = "How does the dataset link to DFO's Program Alignment Architecture (PAA)?"
                list1 = row[field].replace(";", ",").split(",")
                paa_code_list = [paa.code for paa in shared_models.PAAItem.objects.all()]
                for paa in list1:
                    my_code = paa.lstrip().split(" ")[0]
                    if my_code in paa_code_list:
                        r.paa_items.add(shared_models.PAAItem.objects.get(code=my_code))

            i += 1


def update_odi_dates():
    with open(os.path.join(target_dir, "annette_report.csv"), 'r') as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)
        i = 0

        for row in my_csv:
            # only start on row #2
            if i >= 1:
                # most important thing is to establish a uuid. I have verified that the On OGP field is a reliable way to get the uuid
                # i also verified that the best field to get the url / uuid would be row["Location (if yes):"]
                try:
                    r = models.Resource.objects.get(odi_id=row["ref_number"])

                # if created:
                #     print("bad one:", row["title_en"], row["ref_number"], row["portal_url_en"])
                #
                #     r.notes = f'{timezone.now().strftime("%B %d, %Y")}: This record was present on the ODIP winter report but was not in the main OD inventory spreadsheet. ' \
                #               f'I (DJF) am adding Annette Anthony as custodian until proper metadata contacts are identified.'
                #
                #     r.title_eng = row["title_en"]
                #     r.title_fre = row["title_fr"]
                #     r.descr_eng = row["description_en"]
                #     r.descr_fre = row["description_fr"]
                #     r.public_url = row["portal_url_en"]
                #     if len(row["portal_url_en"].split("/")) > 1:
                #         r.uuid = row["portal_url_en"].split("/")[-1]
                #
                #     if row["date_published"]:
                #         r.od_publication_date = make_aware(datetime.datetime.strptime(row["date_published"].lstrip(), "%Y-%m-%d"))
                #     if row["date_released"]:
                #         r.od_release_date = make_aware(datetime.datetime.strptime(row["date_released"].lstrip(), "%Y-%m-%d"))
                #
                #     r.save()
                #
                #     my_user = get_create_user("Annette.Anthony@dfo-mpo.gc.ca")
                #     my_role = models.PersonRole.objects.get(id=1)  # steward
                #     models.ResourcePerson.objects.get_or_create(
                #         resource=r,
                #         person_id=my_user.id,
                #         role=my_role
                #     )
                #
                #     field = "program_alignment_architecture_en"
                #     list1 = row[field].replace(";", ",").split(",")
                #     paa_code_list = [paa.code for paa in shared_models.PAAItem.objects.all()]
                #     for paa in list1:
                #         my_code = paa.lstrip().split(" ")[0]
                #         if my_code in paa_code_list:
                #             r.paa_items.add(shared_models.PAAItem.objects.get(code=my_code))
                #

                except models.Resource.DoesNotExist:
                    # simply add dates
                    save_me = False
                    if not r.od_publication_date and row["date_published"]:
                        r.od_publication_date = make_aware(datetime.datetime.strptime(row["date_published"].lstrip(), "%Y-%m-%d"))
                        save_me = True
                    if not r.od_release_date and row["date_released"]:
                        r.od_release_date = make_aware(datetime.datetime.strptime(row["date_released"].lstrip(), "%Y-%m-%d"))
                        save_me = True
                    if save_me:
                        r.save()
            i += 1
        print(i)


def check_urls():
    for r in models.Resource.objects.filter(odi_id__isnull=False):
        # if r.public_url and "open.canada.ca/" not in r.public_url:
        #     print(r.id, r.public_url, "accessible: " f'http://dmapps/en/inventory/{r.id}/edit/')

        # check if fgp url to be found in notes
        if not r.fgp_url and "https://gcgeo.gc.ca/geone" in r.notes:
            print(r.id, "accessible: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url')


def check_uuids():
    uuid_problem_list = list()
    resource_problem_list = list()
    for r in models.Resource.objects.all():
        if models.Resource.objects.filter(uuid=r.uuid).count() > 1:
            resource_problem_list.append(r.id)
            uuid_problem_list.append(r.uuid)
    print(set(uuid_problem_list))


def regen_uuids():
    my_list = ['f9b277a390534818aa305f772dc97a16',
               '9fe3af482fa0922c41465ef6422a66b5',
               'b8945c0bcb16dc6ed1e58c19749a44cc',
               '8624ad73d65c374d966d9e85d44350bd',
               'c13a752be81b67735193e174db4a4105',
               'c4de6d6cc31e4cfa81fa37c169e27bdc',
               'a839b7e4ad4604fb9948cd18617a76ef',
               '933917e4c64e99618aed08e6a8875641',
               '73ab9c2c3e11c672231b8837bb6eb1ab',
               '0664fca6b457e2a52316e87f3664828e',
               'b07f55f137754029bda2e725da8be5d1',
               '4b6cb7165b5c29e4e2f99e94d17b4668',
               '86dcabf576a368c868397ad65428395d',
               'af74b18a6ef141b99dc89b18197b6bec',
               '8ea7a1bb7235c18bc5fcaed62eca6032',
               '83eefd6cf43a05a2246854c566d6ba6e',
               'dc320263fd9b240ccc578c8335958691',
               '98913402688c16159895ec96b214be5a',
               '682abd8e392346faae3b9d4c6ef9de81',
               'c44745173d9be581a6e2e95273f2058e']
    for target_uuid in my_list:
        # go through once and see if there is a problem

        for r in models.Resource.objects.filter(uuid=target_uuid):
            if r.fgp_url or r.public_url:
                pass
            else:
                r.uuid = uuid.uuid1()
                r.save()


def give_new_uuids():
    r = models.Resource.objects.get(id=445)
    r.uuid = uuid.uuid1()
    r.save()


# def check_uuid_and_urls():
#     for r in models.Resource.objects.all():
#         if models.Resource.objects.filter(uuid=r.uuid).count() > 1:
#             resource_problem_list.append(r.id)
#             uuid_problem_list.append(r.uuid)
#     print(set(uuid_problem_list))

def check_regions():
    for r in models.Resource.objects.filter(odi_id__isnull=False):

        # check if fgp url to be found in notes
        if not r.section:

            if "region: Centr" in r.notes:
                r.section_id = 52
                r.save()
            elif "region: Gulf" in r.notes:
                r.section_id = 26
                r.save()
            elif "region: Mari" in r.notes:
                r.section_id = 106
                r.save()
            elif "region: Que" in r.notes:
                r.section_id = 105
                r.save()
            elif "region: NCR" in r.notes:
                r.section_id = 107
                r.save()
            elif "region: Newfoundland" in r.notes:
                r.section_id = 103
                r.save()
            else:
                print(r.notes)


def check_url_and_uuid():
    for r in models.Resource.objects.all():
        # look for mismatch between uuid and url
        if r.fgp_url or r.public_url:
            if r.fgp_url and str(r.uuid) not in r.fgp_url:
                # print(r.uuid, r.fgp_url)
                # print(r.id, "accessible: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url')
                print(r.fgp_url.split("/")[-1])
                r.uuid = r.fgp_url.split("/")[-1]
                r.save()

            if r.public_url and str(r.uuid) not in r.public_url:
                print(r.uuid, r.public_url)
                print(r.id, "accessible: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url')
                # print(r.fgp_url.split("/")[-1])
                # r.uuid = r.fgp_url.split("/")[-1]
                # r.save()



def test_fgp_urls():
    
    # TODO: 1) check for any FGP datasets that are not declared 1a) published (i.e. 200 response) and non-published (404). Fields should be updated accordingly
    # TODO: 2) check all the public_urls and make sure if present and reachable via 200 response there is a pub date.
    
    for r in models.Resource.objects.all():
        if r.public_url:
            try:
                r1 = requests.get(r.public_url)
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                print("PROBLEM WITH OD URL: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url', "public_url = ", r.public_url)
            except requests.exceptions.ConnectionError:
                print("PROBLEM CONNECTING TO: ", r.public_url, ". We should try again...")
            else:
                if not r1.status_code == 200:
                    print("PROBLEM WITH OD STATUS CODE: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url', "status code = ", r1.status_code, "public_url = ", r.public_url)

        if r.fgp_url:
            try:
                r1 = requests.get(r.fgp_url)
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                print("PROBLEM WITH FGP URL: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url', "fgp_url = ", r.fgp_url)
            except requests.exceptions.ConnectionError:
                print("PROBLEM CONNECTING TO: ", r.public_url, ". We should try again...")
            else:
                if not r1.status_code == 200:
                    print("PROBLEM WITH FGP STATUS CODE: " f'http://dmapps/en/inventory/{r.id}/edit/#id_fgp_url', "status code = ", r1.status_code, "fgp_url = ", r.fgp_url)
