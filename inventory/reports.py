import shutil

import xlsxwriter as xlsxwriter
from django.template.defaultfilters import yesno
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _

from lib.functions.custom_functions import listrify
from lib.templatetags.custom_filters import nz
from lib.templatetags.verbose_names import get_verbose_label, get_field_value
from . import models
from . import xml_export
import os
from shared_models import models as shared_models


def generate_batch_xml(sections):
    # figure out the filenames etc..
    #################################
    # this will be the target dir of the zipfile
    zip_dir = os.path.join(settings.BASE_DIR, 'media', 'inventory', 'temp')
    # this is the filename for the zip file (the zipping function will include the .zip extention)
    zip_filename = "temp_export_{}".format(timezone.now().strftime("%Y-%m-%d"))
    # this is the full path to the target zip file
    zip_file_path = os.path.join(zip_dir, zip_filename)
    # this is the url to the target zip file.. is what is returned by the function
    target_url = os.path.join(settings.MEDIA_ROOT, 'inventory', 'temp', "{}.zip".format(zip_filename))
    # this will be the target dir of the xml files
    xml_dir = os.path.join(settings.BASE_DIR, 'media', 'inventory', 'temp', 'zipdir')

    # clean out the zip_dir directory and subdir
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            os.remove(os.path.join(root, file))

    # start with all resources
    resource_list = models.Resource.objects.all()
    # parse out the sections arg and refine the list
    if sections != "None":
        section_list = [shared_models.Section.objects.get(pk=int(obj)) for obj in sections.split(",")]
        resource_list = [resource for resource in resource_list if resource.section in section_list]

    # generate an xml file for each resource in resource_list
    for resource in resource_list:
        # get the xml data
        xml_data = xml_export.construct(resource, pretty=False)
        # figure out the filename
        xml_filename = "xml_metadata_export_{}.xml".format(resource.id)
        target_file_path = os.path.join(xml_dir, xml_filename)
        # write xml data to file
        xml_data.write(target_file_path)

    # zip the folder
    # adapted from https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    shutil.make_archive(zip_file_path, 'zip', xml_dir)

    return target_url


def generate_odi_report():
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'inventory', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'inventory', 'temp', target_file)
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    # create formatting variables
    title_format = workbook.add_format(
        {'bold': False, "align": 'normal', 'font_size': 14, "text_wrap": False, 'bg_color': '#006640', 'font_color': 'white'})
    header_format = workbook.add_format(
        {'bold': False, 'border': 1, 'border_color': 'black', 'bg_color': '#A1B7BF', "align": 'normal', "text_wrap": False})

    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, })
    date_format = workbook.add_format({'num_format': "yyyy-mm-dd", "align": 'left', })

    # get the trip list
    resource_list = models.Resource.objects.filter(odi_id__isnull=False)

    field_list = [
        "odi_id",
        "title_eng",
        "title_fre",
        "descr_eng",
        "descr_fre",
        "publisher_en",
        "publisher_fr",
        "od_publication_date",
        "language",
        "size",
        "eligible_for_release",
        "paa_en",
        "paa_fr",
        "od_release_date",
        "url_en",
        "url_fr",
    ]

    # define the headers
    header1 = ["dfo-mpo",
               "Open Data Inventory        Fisheries and Oceans Canada | Pêches et Océans Canada",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               "",
               ]
    header2 = ["Reference Number",
               "Title (English)",
               "Title (French)",
               "Description (English)",
               "Description (French)",
               "Publisher - Name at Publication (English)",
               "Publisher - Name at Publication (French)",
               "Date Published",
               "Language",
               "Size",
               "Eligible for Release",
               "Program Alignment Architecture (English)",
               "Program Alignment Architecture (French)",
               "Date Released",
               "Open Government Portal Record (English)",
               "Open Government Portal Record (French)", ]
    header3 = ["ref_number",
               "title_en",
               "title_fr",
               "description_en",
               "description_fr",
               "publisher_en",
               "publisher_fr",
               "date_published",
               "language",
               "size",
               "eligible_for_release",
               "program_alignment_architecture_en",
               "program_alignment_architecture_fr",
               "date_released",
               "portal_url_en",
               "portal_url_fr",
               ]
    # header.append('Number of projects tagged')

    # define a worksheet
    my_ws = workbook.add_worksheet(name="trip list")
    my_ws.write_row(0, 0, header1, title_format)
    my_ws.write_row(1, 0, header2, header_format)
    my_ws.write_row(2, 0, header3, header_format)
    my_ws.set_row(2, 0)  # row # 2 is a hidden row

    i = 3
    for r in resource_list.order_by("odi_id"):
        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header2]

        j = 0
        for field in field_list:

            if "publisher_en" in field:
                my_val = "Fisheries and Oceans"
                my_ws.write(i, j, my_val, normal_format)

            elif "publisher_fr" in field:
                my_val = "Pêches et Océans"
                my_ws.write(i, j, my_val, normal_format)

            elif "eligible_for_release" in field:
                my_val = "Y"
                my_ws.write(i, j, my_val, normal_format)

            elif "language" in field:
                my_val = "en+fr" if r.od_publication_date else ""
                my_ws.write(i, j, my_val, normal_format)

            elif "paa_en" in field:
                my_val = listrify([f'{paa.code} {paa.name}' for paa in r.paa_items.all()])
                my_ws.write(i, j, my_val, normal_format)

            elif "paa_fr" in field:
                my_val = listrify([f'{paa.code} {paa.nom}' for paa in r.paa_items.all()])
                my_ws.write(i, j, my_val, normal_format)

            elif "url_en" in field:
                if r.public_url:
                    my_val = f'https://open.canada.ca/data/en/dataset/{r.uuid}'
                else:
                    my_val = ""
                my_ws.write_url(i, j, url=my_val, string=my_val)
            elif "url_fr" in field:
                if r.public_url:
                    my_val = f'https://ouvert.canada.ca/data/fr/dataset/{r.uuid}'
                else:
                    my_val = ""
                my_ws.write_url(i, j, url=my_val, string=my_val)
            elif "date" in field:
                my_val = get_field_value(r, field, nullmark="")
                my_ws.write(i, j, my_val, date_format)
            else:
                my_val = get_field_value(r, field, nullmark="")
                my_ws.write(i, j, my_val, normal_format)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            # if new value > stored value... replace stored value
            if len(str(my_val)) > col_max[j]:
                if len(str(my_val)) < 75:
                    col_max[j] = len(str(my_val))
                else:
                    col_max[j] = 75
            j += 1
        i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_physical_samples_report():
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'inventory', 'temp')
    target_file = "temp_data_export_{}.xlsx".format(timezone.now().strftime("%Y-%m-%d"))
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'inventory', 'temp', target_file)
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    # create formatting variables
    title_format = workbook.add_format(
        {'bold': False, "align": 'normal', 'font_size': 14, "text_wrap": False, 'bg_color': '#006640', 'font_color': 'white'})
    header_format = workbook.add_format(
        {'bold': False, 'border': 1, 'border_color': 'black', 'bg_color': '#A1B7BF', "align": 'normal', "text_wrap": False})

    normal_format = workbook.add_format({"align": 'left', "text_wrap": True, })
    date_format = workbook.add_format({'num_format': "yyyy-mm-dd", "align": 'left', })

    # get the resource list
    # anything with resource type as "physical collection"
    ids = [r.id for r in models.Resource.objects.filter(resource_type_id=4)]
    # anything where this is a meaningful description of physical samples
    ids.extend(
        [r.id for r in models.Resource.objects.filter(physical_sample_descr_eng__isnull=False) if len(r.physical_sample_descr_eng) > 10])
    ids.extend(
        [r.id for r in models.Resource.objects.filter(physical_sample_descr_fre__isnull=False) if len(r.physical_sample_descr_fre) > 10])
    # anything where the word "physical" is in the title
    ids.extend(
        [r.id for r in models.Resource.objects.filter(title_eng__icontains="physical").filter(title_eng__icontains="sample")])
    ids.extend(
        [r.id for r in models.Resource.objects.filter(title_fre__icontains="physique").filter(title_fre__icontains="échantillon")])
    # anything where the word "physical" is in the storage notes
    ids.extend(
        [r.id for r in models.Resource.objects.filter(storage_envr_notes__icontains="physical").filter(storage_envr_notes__icontains="sample")])
    ids.extend(
        [r.id for r in models.Resource.objects.filter(storage_envr_notes__icontains="physique").filter(storage_envr_notes__icontains="échantillon")])


    resources = models.Resource.objects.filter(id__in=ids)

    field_list = [
        "id",
        "title_eng",
        "title_fre",
        "physical_sample_descr_eng",
        "physical_sample_descr_fre",
        "storage_envr_notes",
        "hyperlink",
    ]

    # define the headers
    header0 = ["dfo-mpo",
               "Physical Samples Report        Fisheries and Oceans Canada | Pêches et Océans Canada",
               "",
               "",
               "",
               "",
               "",
               ]
    header = [get_verbose_label(resources.first(), field) for field in field_list]

    # header.append('Number of projects tagged')

    # define a worksheet
    my_ws = workbook.add_worksheet(name="query results")
    my_ws.write_row(0, 0, header0, title_format)
    my_ws.write_row(2, 0, header, header_format)

    i = 3
    for r in resources.order_by("id"):
        # create the col_max column to store the length of each header
        # should be a maximum column width to 100
        col_max = [len(str(d)) if len(str(d)) <= 100 else 100 for d in header]

        j = 0
        for field in field_list:
            if "hyperlink" in field:
                my_val = f'http://dmapps{reverse("inventory:resource_detail", args=[r.id])}'
                my_ws.write_url(i, j, url=my_val, string=my_val)
            else:
                my_val = get_field_value(r, field, nullmark="")
                my_ws.write(i, j, my_val, normal_format)

            # adjust the width of the columns based on the max string length in each col
            ## replace col_max[j] if str length j is bigger than stored value

            # if new value > stored value... replace stored value
            if len(str(my_val)) > col_max[j]:
                if len(str(my_val)) < 75:
                    col_max[j] = len(str(my_val))
                else:
                    col_max[j] = 75
            j += 1
        i += 1

        # set column widths
        for j in range(0, len(col_max)):
            my_ws.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url
