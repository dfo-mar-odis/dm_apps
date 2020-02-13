import os
import xml.etree.ElementTree as ET

from django.contrib.auth.models import User

from inventory import models
from django.conf import settings


def create_user(email):
    # if it is a DFO email, then it should be easy..
    email = email.lower()
    names = email.split("@")[0].split(".")
    first_name = names[0]
    last_name = names[-1]
    # print(email, first_name, last_name, names)
    my_user = User.objects.create(
        username=email,
        first_name=first_name.title(),
        last_name=last_name.title(),
        password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
        is_active=0,
        email=email,
    )
    print("new user created:", my_user.email)
    return my_user


def restart():
    models.Resource.objects.filter(section_id=61).delete()


def check_uuids():
    target_dir = os.path.join(settings.BASE_DIR, 'inventory', 'temp')
    # with open(os.path.join(target_dir, "QuiderE_v2b.xml"), 'r', encoding="utf8") as xml_file:
    # with open(os.path.join(target_dir, "JacobsK_v2b.xml"), 'r') as xml_file:
    # with open(os.path.join(target_dir, "PED_Records_Output_v3.xml"), 'r') as xml_file:
    with open(os.path.join(target_dir, "BondSRecords_Output.xml"), 'r') as xml_file:

        tree = ET.parse(xml_file)
        recordset = tree.getroot()
        my_dict = {}
        for record in recordset:
            uuid = record.find("record_uuid").text
            if not my_dict.get(uuid):
                my_dict[uuid] = 0
            my_dict[uuid] += 1

        for uuid in my_dict:
            if my_dict[uuid] > 1:
                print(uuid, my_dict[uuid])


def import_xml():
    target_dir = os.path.join(settings.BASE_DIR, 'inventory', 'temp')
    # with open(os.path.join(target_dir, "QuiderE_v2b.xml"), 'r', encoding="utf8") as xml_file:
    #     section_id = 52
    # with open(os.path.join(target_dir, "JacobsK_v2b.xml"), 'r') as xml_file:
    #     section_id = 51
    # with open(os.path.join(target_dir, "PED_Records_Output_v3.xml"), 'r', encoding="utf8") as xml_file:
    #     section_id = 59
    # with open(os.path.join(target_dir, "BondSRecords_Output.xml"), 'r', encoding="utf8") as xml_file:
    #     section_id = 60
    with open(os.path.join(target_dir, "MetadataCardosoD_20200205a.xml"), 'r', encoding="utf8") as xml_file:
        section_id = 61
    # with open(os.path.join(target_dir, "MetadataKraskaP_20200206a.xml"), 'r', encoding="utf8") as xml_file:
    #     section_id = 62
        if section_id == 51:
            uuid_list = [
                "3659734a-3b89-4f9a-8558-f5dde61a7350",  # 2
                "",
                "b63de91e-71b8-4ec6-9e09-a12cb2fbf758",  # 2
                "",
                "750b5f56-292c-4e4e-9b22-2644e2a463f4",  # 2
                "",
                "5215563c-48f3-4e3b-8c27-b40c5221f368",  # 2
                "",
                "682abd8e-3923-46fa-ae3b-9d4c6ef9de81",  # 2
                "",
                "af74b18a-6ef1-41b9-9dc8-9b18197b6bec",  # 6
                "",
                "",
                "",
                "",
                "",
                "b07f55f1-3775-4029-bda2-e725da8be5d1",  # 4
                "",
                "",
                "",
                "a24e1b55-5441-4b5a-8d3f-dfa8f3e4123a",  # 2
                "",
                "c4de6d6c-c31e-4cfa-81fa-37c169e27bdc",  # 7
                "",
                "",
                "",
                "",
                "",
                "",
                "e7c6115f-8ae3-4bb0-9bfa-3ba0fb725d2f",  # 2
                "",
                "146ed171-8ce1-4f8a-b983-baf16ba3150f",  # 2
                "",
                "9ff019fc-1235-42b0-b7d9-ff96dfa3a3c7",  # 2
                "",
                "f48d8fbe-b1c0-4023-9727-de8769b1dbb6",  # 2
                "",
                "7035da9a-adf3-44e6-ae87-bce2eac5f7e8",  # 2
                "",
                "e036dec8-6479-4324-b9b1-0e264b7bbdb3",  # 2
                "",
                "614065d0-8ed2-4142-924a-cdc0689362b3",  # 2
                "",
                "9192f25a-0006-48f8-ad24-6db1913845be",  # 2
                "",
                "8b8e0e28-ea4d-4c53-bd3d-856dca19616c",  # 2
                "",
                "0c2a74d7-e511-45d8-bcda-9eaf15c59ea3",  # 2
                "",
                "a29af2e1-d205-4d1d-9051-24a3454ff0b7",  # 2
                "",
                "a59aa9af-b636-48d4-892f-872cff3acbc1",  # 2
                "",
                "12ef1e35-3b4a-4750-9004-ecb40c6d5216",  # 2
                "",
                "9405112b-9b3a-4beb-bb32-c52653790538",  # 2
                "",
                "23319b68-d6f5-4523-8561-6e282a07c08d",  # 2
                "",
                "b65b16ad-7554-4e50-9650-ff6b1bd75293",  # 2
                "",
                "5d94ca72-1843-4c41-a715-b1f40b44fff6",  # 2
                "",
                "4d5bf4e4-3889-4a96-89a0-59fd309dbde4",  # 2
                "",
                "eb18c77a-7630-4a6b-9217-f4a6dd26198b",  # 2
                "",
                "bcd0c49c-3244-4e31-a2f7-c921c7c8c5b2",  # 2
                "",
                "f9b277a3-9053-4818-aa30-5f772dc97a16",  # 3
                "",
                "",
                "ba674977-9a60-4f2e-8012-a1b86583ab8e",  # 2
                "",
            ]


        tree = ET.parse(xml_file)
        recordset = tree.getroot()
        time_period_list = []
        org_list = []
        count = 0
        for record in recordset:
            # identifying fields; these should never change, no matter how many times we do the import
            uuid = record.find("record_uuid").text

            if uuid:
                title = record.find("record_title").text
                title_fra = record.find("record_title_fra").text if record.find("record_title_fra") is not None else None
                desc = record.find("record_abstract").text if record.find("record_abstract") is not None else None
                desc_fra = record.find("record_abstract_fra").text if record.find("record_abstract_fra") is not None else None
                purpose = record.find("record_purpose").text if record.find("record_purpose") is not None else None
                purpose_fra = record.find("record_purpose_fra").text if record.find("record_purpose_fra") is not None else None
                geo_desc = record.find("record_geographic_extent_geodescription").text if record.find(
                    "record_geographic_extent_geodescription") else None

                prim_lang = record.find("record_primary_language").text if record.find("record_primary_language") is not None else None
                series = record.find("record_series").text if record.find("record_series") is not None else None
                suppl_info = record.find("record_supplemental_info").text if record.find("record_supplemental_info") is not None else None
                suppl_info_fra = record.find("record_supplemental_info_fra").text if record.find("record_supplemental_info_fra") is not None else None

                if record.find("record_geographic_extent_boundingbox") is not None:
                    geo_bbox_w = record.find("record_geographic_extent_boundingbox").find('record_extent_west').text if record.find(
                        "record_geographic_extent_boundingbox").find('record_extend_west') is not None else None
                    geo_bbox_e = record.find("record_geographic_extent_boundingbox").find('record_extend_east').text if record.find(
                        "record_geographic_extent_boundingbox").find('record_extend_east') is not None else None
                    geo_bbox_s = record.find("record_geographic_extent_boundingbox").find('record_extend_south').text if record.find(
                        "record_geographic_extent_boundingbox").find('record_extend_south') is not None else None
                    geo_bbox_n = record.find("record_geographic_extent_boundingbox").find('record_extend_north').text if record.find(
                        "record_geographic_extent_boundingbox").find('record_extend_north') is not None else None
                else:
                    geo_bbox_e = None
                    geo_bbox_s = None
                    geo_bbox_n = None
                    geo_bbox_w = None
                storage_envr_notes = record.find("record_dataset-uri").text if record.find("record_dataset-uri") is not None else None

                # THINGS THAT will require some creativity

                # resource constraints
                if record.find("record_other_constraints") is not None:
                    if record.find("record_other_constraints").find("record_other_constraint") is not None:
                        resource_constraints = record.find("record_other_constraints").find("record_other_constraint").text
                    else:
                        resource_constraints = None
                else:
                    resource_constraints = None

                # status
                if record.find("record_status") is not None:
                    if record.find("record_status").find("record_status_code") is not None:
                        status_text = record.find("record_status").find("record_status_code").text
                    else:
                        status_text = None
                else:
                    status_text = None

                if status_text:
                    try:
                        my_status = models.Status.objects.get(label__icontains=status_text)
                    except models.Status.DoesNotExist:
                        try:
                            my_status = models.Status.objects.get(code__iexact=status_text)
                        except models.Status.DoesNotExist:
                            print("bad status:", status_text)
                            my_status = models.Status.objects.create(
                                label=status_text,
                                code=status_text,
                            )
                else:
                    my_status = None

                # Security classification
                if record.find("record_security_constraint") is not None:
                    if record.find("record_security_constraint").find("record_security_constraint_code") is not None:
                        security_classification = record.find("record_security_constraint").find("record_security_constraint_code").text
                    else:
                        security_classification = None
                else:
                    security_classification = None

                if security_classification:
                    try:
                        my_security_classification = models.SecurityClassification.objects.get(label__icontains=security_classification)
                    except models.SecurityClassification.DoesNotExist:
                        try:
                            my_security_classification = models.SecurityClassification.objects.get(code__iexact=security_classification)
                        except models.SecurityClassification.DoesNotExist:
                            print("bad security classification:", security_classification)
                            my_security_classification = models.SecurityClassification.objects.create(
                                label=security_classification,
                                code=security_classification,
                            )
                else:
                    my_security_classification = None

                # Use limitation
                if record.find("record_use_contraints") is not None:
                    if record.find("record_use_contraints").find("record_use_constraint").find("record_use_constraint_label") is not None:
                        # security_classification = record.find("record_security_constraint").find("record_security_constraint_code").text
                        use_limitation = record.find("record_use_contraints").find("record_use_constraint").find(
                            "record_use_constraint_label").text
                        use_limitation += " (" + record.find("record_use_contraints").find("record_use_constraint").find(
                            "record_use_constraint_codelist").text + ")"
                    else:
                        use_limitation = None
                else:
                    use_limitation = None

                # Start and End of Records
                if record.find("record_time_period") is not None:
                    start = record.find("record_time_period").find("begin").text if record.find("record_time_period").find(
                        "begin") is not None else None
                    end = record.find("record_time_period").find("end").text if record.find("record_time_period").find(
                        "end") is not None else None
                else:
                    start = None
                    end = None

                start_year = None
                start_month = None
                start_day = None

                if start:
                    # a couple of different formats.. "yyyy-mm-dd" or "yyyy yyyy" or  "yyyy" or "July and August 2004" ...
                    start_list = start.split("-")

                    # let's start with the easy scenario: yyyy-mm-dd
                    if len(start_list) >= 3:
                        if len(start_list) == 3 and len(start_list[0]) == 4 and len(start_list[1]) == 2 and len(start_list[2]) == 2:
                            start_year = int(start_list[0])
                            start_month = int(start_list[1]) if int(start_list[1]) <= 12 else None
                            start_day = int(start_list[2]) if int(start_list[2]) <= 31 else None

                        else:
                            print(start_list)
                            # # there is special case when two full years are provided
                            start_list = start.split(" ")

                            # which year is smallest?
                            year1 = start_list[0].split("-")[0]
                            year2 = start_list[1].split("-")[0]
                            if len(year1) == 4 and (year1.startswith("1") or year1.startswith("2")):
                                if len(year2) == 4 and (year2.startswith("1") or year2.startswith("2")):
                                    index = 0 if int(year1) < int(year2) else 1
                                else:
                                    index = 1
                            elif len(year2) == 4 and (year2.startswith("1") or year2.startswith("2")):
                                index = 0
                            else:
                                index = None
                                print("don't know how to get date")

                            if index:
                                start_year = int(start_list[index].split("-")[0])
                                start_month = int(start_list[index].split("-")[1])
                                start_day = int(start_list[index].split("-")[2])
                    # less common scenario where we have: yyyy-mm
                    elif len(start_list) == 2:
                        if len(start_list[0]) == 4 and len(start_list[1]) == 2:
                            start_year = int(start_list[0])
                            start_month = int(start_list[1]) if int(start_list[1]) <= 12 else None


                    elif len(start_list) == 1:
                        start_list = start.split(" ")
                        # simple yyyy etc
                        if len(start_list[0]) == 4 and (start_list[0].startswith("1") or start_list[0].startswith("2")):
                            try:
                                start_year = int(start_list[0])
                            except (TypeError, ValueError):
                                pass
                        # lets just try and get a year
                        else:
                            for item in start_list:
                                if len(item) == 4 and (item.startswith("1") or item.startswith("2")):
                                    try:
                                        temp_year = int(item)
                                        # print(temp_year)
                                        if not start_year:
                                            start_year = temp_year
                                        elif start_year > temp_year:
                                            start_year = temp_year
                                        # print("my_year:", year)
                                    except TypeError:
                                        print("not a good integer")
                            if not start_year:
                                time_period_list.append(start)
                    else:
                        time_period_list.append(start)

                end_year = None
                end_month = None
                end_day = None
                if end:
                    # a couple of different formats.. "yyyy-mm-dd" or "yyyy yyyy" or  "yyyy" or "July and August 2004" ...
                    end_list = end.split("-")

                    # let's start with the easy scenario: yyyy-mm-dd
                    if len(end_list) >= 3:
                        if len(end_list) == 3 and len(end_list[0]) == 4 and len(end_list[1]) == 2 and len(end_list[2]) == 2:
                            end_year = int(end_list[0])
                            end_month = int(end_list[1]) if int(end_list[1]) <= 12 else None
                            end_day = int(end_list[2]) if int(end_list[2]) <= 31 else None

                        else:
                            # # there is special case when two full years are provided
                            end_list = end.split(" ")

                            # which year is smallest?
                            year1 = end_list[0].split("-")[0]
                            year2 = end_list[1].split("-")[0]
                            if len(year1) == 4 and (year1.startswith("1") or year1.startswith("2")):
                                if len(year2) == 4 and (year2.startswith("1") or year2.startswith("2")):
                                    index = 0 if int(year1) < int(year2) else 1
                                else:
                                    index = 1
                            elif len(year2) == 4 and (year2.startswith("1") or year2.startswith("2")):
                                index = 0
                            else:
                                index = None
                                print("don't know how to get date")

                            if index:
                                end_year = int(end_list[index].split("-")[0])
                                end_month = int(end_list[index].split("-")[1])
                                end_day = int(end_list[index].split("-")[2])

                    # less common scenario where we have: yyyy-mm
                    elif len(end_list) == 2:
                        if len(end_list[0]) == 4 and len(end_list[1]) == 2:
                            end_year = int(end_list[0])
                            end_month = int(end_list[1]) if int(end_list[1]) <= 12 else None

                    elif len(end_list) == 1:
                        end_list = end.split(" ")
                        # simple yyyy etc
                        if len(end_list[0]) == 4 and (end_list[0].startswith("1") or end_list[0].startswith("2")):
                            try:
                                end_year = int(end_list[0])
                            except (TypeError, ValueError):
                                pass
                        # lets just try and get a year
                        else:
                            for item in end_list:
                                if len(item) == 4 and (item.startswith("1") or item.startswith("2")):
                                    try:
                                        temp_year = int(item)
                                        # print(temp_year)
                                        if not end_year:
                                            end_year = temp_year
                                        elif end_year > temp_year:
                                            end_year = temp_year
                                        # print("my_year:", year)
                                    except TypeError:
                                        print("not a good integer")
                            if not end_year:
                                time_period_list.append(end)
                    else:
                        time_period_list.append(end)

                notes = "This record was imported into DMApps from metadata files generated by JMetaWriter. " \
                        "The core information from the original XML files were successfully extracted however " \
                        "some of the more nuanced aspects of the original metadata may not have been captured in this process. " \
                        "Accordingly, the original XML file should be retained on record. " \
                        "Tobias Spears (BIO) was responsible for the XML transformation and David Fishman (GFC) was responsible " \
                        "for the import of the transformed data into the DM Apps database."

                # if uuid == "cacb5897-f59d-4b18-a8ab-e34eec0e181b":
                if prim_lang:
                    notes += " || PRIMARY LANGUAGE: {}".format(prim_lang)
                if series:
                    notes += " || SERIES: {}".format(series)
                if suppl_info:
                    notes += " || SUPPLEMENTAL INFO (ENGLISH): {}".format(suppl_info)
                if suppl_info_fra:
                    notes += " || SUPPLEMENTAL INFO (FRENCH): {}".format(suppl_info_fra)

                try:
                    my_resource, created = models.Resource.objects.get_or_create(uuid=uuid, )
                except models.Resource.MultipleObjectsReturned:
                    # delete any pre-existing records (ruthless)
                    models.Resource.objects.filter(uuid=uuid).delete()
                    # try again
                    my_resource, created = models.Resource.objects.get_or_create(uuid=uuid, )


                if created:
                    print("creating new record", uuid)

                my_resource.title_eng = title
                my_resource.title_fre = title_fra if title_fra else None
                my_resource.purpose_eng = ' '.join(purpose.split()) if purpose else None
                my_resource.purpose_fre = ' '.join(purpose_fra.split()) if purpose_fra else None
                my_resource.descr_eng = ' '.join(desc.split()) if desc else None
                my_resource.descr_fre = ' '.join(desc_fra.split()) if desc_fra else None
                my_resource.geo_descr_eng = ' '.join(geo_desc.split()) if geo_desc else None
                my_resource.section_id = section_id
                my_resource.notes = ' '.join(notes.split()) if notes else None
                my_resource.east_bounding = geo_bbox_e
                my_resource.north_bounding = geo_bbox_n
                my_resource.south_bounding = geo_bbox_s
                my_resource.west_bounding = geo_bbox_w
                my_resource.status = my_status
                my_resource.time_start_year = start_year
                my_resource.time_start_month = start_month
                my_resource.time_start_day = start_day
                my_resource.time_end_year = end_year
                my_resource.time_end_month = end_month
                my_resource.time_end_day = end_day
                my_resource.storage_envr_notes = ' '.join(storage_envr_notes.split()) if storage_envr_notes else None
                my_resource.security_classification = my_security_classification
                my_resource.security_use_limitation_eng = ' '.join(use_limitation.split()) if use_limitation else None
                my_resource.resource_constraint_eng = ' '.join(resource_constraints.split()) if resource_constraints else None
                my_resource.save()

                # ISO Topic Categories
                isotopics = record.find("record_iso_topics")
                if isotopics is not None:
                    for topic in isotopics:
                        if topic is not None:
                            if topic.text and len(topic.text.replace(" ", "")) > 1:
                                try:
                                    my_topic = models.Keyword.objects.get(text_value_eng__iexact=topic.text, keyword_domain_id=8)
                                except models.Keyword.DoesNotExist:
                                    print("bad topic:", topic.text, "length:", len(topic.text.replace(" ", "")))
                                    my_topic = models.Keyword.objects.create(
                                        text_value_eng=topic.text,
                                        keyword_domain_id=8,
                                        concept_scheme="isotopiccategory"
                                    )
                                finally:
                                    my_resource.keywords.add(my_topic)

                # GCMD
                keywords = record.find("record_keywords")
                if keywords is not None:
                    for group in keywords:
                        for kw in group:
                            if kw.tag == "record_keyword":
                                if kw.find("record_keyword_eng") is not None:
                                    kw_text = kw.find("record_keyword_eng").text
                                    my_kw = None
                                    try:
                                        my_kw = models.Keyword.objects.get(text_value_eng__icontains=kw_text)
                                        # print('good!', my_kw)
                                    except (models.Keyword.DoesNotExist, ValueError):
                                        print("bad topic:", kw_text)
                                        # my_kw = models.Keyword.objects.create(
                                        #     text_value_eng=kw_text,
                                        #     keyword_domain_id=1,
                                        #     concept_scheme="theme"
                                        # )
                                        my_kw = None
                                    except models.Keyword.MultipleObjectsReturned:
                                        my_kw = models.Keyword.objects.filter(text_value_eng__icontains=kw_text).first()
                                        # print("many hits:", kw_text, "first one: ", my_kw)
                                    finally:
                                        if my_kw:
                                            my_resource.keywords.add(my_kw)

                                # else:
                                #     print("different kind of keyword was encountered.")
                # Contacts
                metadata_contacts = record.find("record_contact_metadata")
                citation_contacts = record.find("record_citation_contact_metadata")
                distributor_contacts = record.find("record_distributor_contact_metadata")
                all_contact_list = [metadata_contacts, citation_contacts, distributor_contacts]

                for contact_list in all_contact_list:
                    if contact_list is not None:
                        for contact in contact_list:
                            # find the role
                            xml_role = contact.find("record_contact_role").find("record_contact_role_code").text if contact.find(
                                "record_contact_role") is not None else None
                            if xml_role and len(xml_role.replace(" ", "")) > 1:
                                try:
                                    my_role = models.PersonRole.objects.get(role__istartswith=xml_role[:3])
                                except models.PersonRole.DoesNotExist:
                                    try:
                                        my_role = models.PersonRole.objects.get(code__iexact=xml_role)
                                    except models.PersonRole.DoesNotExist:
                                        print("bad role:", xml_role, "need to create a new one.")
                                        my_role = models.PersonRole.objects.create(
                                            role=xml_role,
                                            code=xml_role,
                                        )
                            else:
                                my_role = None

                            # see if the person already exists in the system. Email address will be the best way to see.

                            if contact.find("record_contact_addresses") is not None:
                                if contact.find("record_contact_addresses").find("record_contact_address") is not None:
                                    if contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_electronic_mail_address") is not None:
                                        email = contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_electronic_mail_address").text
                                    else:
                                        email = None
                                else:
                                    email = None
                            else:
                                email = None

                            if email:
                                try:
                                    my_user = User.objects.get(email__iexact=email)
                                except User.DoesNotExist:
                                    # print(email, "is not present in db")
                                    my_user = create_user(email)
                            else:
                                my_user = None

                            # Build up the person attached to the user... address, org
                            if my_user:
                                try:
                                    my_person = models.Person.objects.get(pk=my_user.id)
                                except models.Person.DoesNotExist:
                                    my_person = models.Person.objects.create(pk=my_user.id)

                                if not my_person.phone:
                                    try:
                                        my_phone = contact.find("record_contact_phones").find("record_contact_phone").text
                                        my_person.phone = my_phone
                                        my_person.save()
                                    except AttributeError:
                                        print("no phone number")

                                if not my_person.organization:
                                    # let's see if we can come up with an educated guess about the org
                                    try:
                                        org_name = contact.find("record_contact_organization").text
                                    except AttributeError:
                                        print("no org name")
                                        org_name = None
                                    try:
                                        org_address = contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_delivery_point").text
                                    except AttributeError:
                                        print("no org address")
                                        org_address = None
                                    try:
                                        org_city = contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_city").text
                                    except AttributeError:
                                        print("no org city")
                                        org_city = None
                                    try:
                                        org_prov = contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_administrative_area").text
                                    except AttributeError:
                                        print("no org province")
                                        org_prov = None
                                    try:
                                        org_postal_code = contact.find("record_contact_addresses").find("record_contact_address").find(
                                            "record_contact_postal_code").text
                                    except AttributeError:
                                        print("no org postal code")
                                        org_postal_code = None
                                    # print(org_name, org_address, org_city, org_postal_code, org_prov)

                                    # if we have an org_name, we can continue to play this game...
                                    if org_name:
                                        my_org = None

                                        # in the most common scenario, we are talking about a DFO office...We would need a city in order to decide which office
                                        if "fisheries and oceans" in org_name.lower():
                                            if org_city:
                                                # try to get the office.. if nothing then just create it.
                                                try:
                                                    my_org = models.Organization.objects.get(name_eng__icontains="fisheries and oceans",
                                                                                             city__icontains=org_city.lower()[:3])
                                                except models.Organization.DoesNotExist:
                                                    my_org = models.Organization.objects.create(
                                                        name_eng="Government of Canada; Fisheries and Oceans Canada",
                                                        name_fre="Gouvernement du Canada; Pêches et Océans Canada",
                                                        abbrev="DFO-MPO",
                                                        address=org_address,
                                                        city=org_city,
                                                        postal_code=org_postal_code,
                                                    )
                                            else:
                                                # default to the Winnipeg office
                                                my_org = models.Organization.objects.get(name_eng__icontains="fisheries and oceans",
                                                                                         city__icontains="winn")

                                        else:
                                            # we have to see if the org_name already exists... trickier
                                            try:
                                                my_org = models.Organization.objects.get(name_eng__icontains=org_name.lower())
                                            except models.Organization.DoesNotExist:
                                                # if we cannot find it, create it.
                                                my_org = models.Organization.objects.create(
                                                    name_eng=org_name,
                                                    address=org_address,
                                                    city=org_city,
                                                    postal_code=org_postal_code,
                                                )

                                        # if we were successful, let's add the org to the person
                                        if my_org:
                                            my_person.organization = my_org
                                            my_person.save()
                                        else:
                                            org_list.append(org_name, org_city)

                            # record_contact_organization

                            # make sure the person is attached to the resource
                            if my_user and my_role:
                                my_resource_person, created = models.ResourcePerson.objects.get_or_create(
                                    resource=my_resource,
                                    person_id=my_user.id,
                                    role=my_role
                                )
                            else:
                                # print("problemo", "user: ", my_user, "role: ", my_role)
                                pass
                count += 1

    print(set(time_period_list))
    print(set(org_list))
    print(count, "records added")



def add_custodian():
    # section_id = 52  # elliott
    # section_id = 51  # kevin
    # section_id = 59 # mike
    section_id = 60  # shelley

    for record in models.Resource.objects.filter(section_id=section_id):
        models.ResourcePerson.objects.get_or_create(
            person_id=322,
            resource=record,
            role_id=1,
        )
