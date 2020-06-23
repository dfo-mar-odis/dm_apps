import csv
import os

from django.core import serializers
from django.core.files import File

from inventory import models
from inventory import xml_export
from shared_models import models as shared_models



def export_fixtures():
    """ a simple function to expor the important lookup tables. These fixutre will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fixtures')
    models_to_export = [
        models.Location,
        models.Status,

        models.PersonRole,
        models.SpatialRepresentationType,
        models.SpatialReferenceSystem,
        models.SecurityClassification,
        models.ResourceType,
        models.Maintenance,
        models.CharacterSet,
        models.KeywordDomain,
        models.ContentType,
        shared_models.FiscalYear,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()



def transfer_dist_formats():
    for resource in models.Resource.objects.filter(distribution_format__isnull=False):
        # look for match in other table
        df = models.DistributionFormat.objects.get(name__iexact=resource.distribution_format)
        resource.distribution_formats.add(df)



def resave_all(resources=models.Resource.objects.all()):
    for r in resources:
        xml_export.verify(r)


def import_new_species():
    pass
    # open the csv we want to read
    # rootdir = "C:\\Users\\fishmand\\Desktop\\dump"
    # with open(os.path.join(rootdir, "OntarioFishList.csv"), 'r') as csv_read_file:
    #     my_csv = csv.DictReader(csv_read_file)
    #
    #     for row in my_csv:
    #         tsn = row["TSN"]
    #         if tsn:
    #             # first check to make sure there is not a duplicate entry
    #             if models.Keyword.objects.filter(keyword_domain_id=2, uid=tsn).count() > 0:
    #                 my_kw = models.Keyword.objects.filter(keyword_domain_id=2, uid=tsn).first()
    #                 print("Keyword #{} already has TSN {}".format(my_kw.id, tsn))
    #             else:
    #                 # enter a new keyword
    #                 scientific_name = row["Scientific"]
    #                 common_names = row["common names"]
    #                 new_keyword = models.Keyword.objects.create(
    #                     text_value_eng=scientific_name,
    #                     text_value_fre=scientific_name,
    #                     uid=tsn,
    #                     concept_scheme='species',
    #                     details=common_names,
    #                     is_taxonomic=1,
    #                     keyword_domain_id=2,
    #                 )
    #         else:
    #             # enter a new keyword
    #             scientific_name = row["Scientific"]
    #             common_names = row["common names"]
    #             new_keyword = models.Keyword.objects.create(
    #                 text_value_eng=scientific_name,
    #                 text_value_fre=scientific_name,
    #                 concept_scheme='species',
    #                 details=common_names,
    #                 is_taxonomic=1,
    #                 keyword_domain_id=4,
    #             )
    #             print("'{}' does not have a TSN therefore is being added under the 'uncontrolled vocabulary' keyword domain".format(common_names))
