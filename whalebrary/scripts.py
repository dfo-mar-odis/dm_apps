import csv
import os

from django.conf import settings
from django.core import serializers
from django.core.files import File

from whalebrary import models


# for individual exports, can use:
# python manage.py dumpdata app_name.model_name > whalebrary/fixtures/file.json

#to run this script do:
# python manage.py shell
# from whalebrary.scripts import export_fixtures
# export_fixtures()

def export_fixtures():
    """ a simple function to export the important lookup tables. These fixtures will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    models_to_export = [
        # models.Category,
        # models.GearType,
        # models.Experience,
        # models.TransactionCategory,
        models.Species,
    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w', encoding='utf-8')
        myfile = File(f)
        myfile.write(data)
        myfile.close()


# for importing species data from csv
def import_species_data():
    # open the csv we want to read
    my_target_data_file = os.path.join(settings.BASE_DIR, 'whalebrary', 'misc/species_data.csv')
    with open(my_target_data_file, 'r') as csv_read_file:
        my_csv = csv.DictReader(csv_read_file)

        for column in my_csv:

            # species
            species, created = models.Species.objects.get_or_create(
                name=column["name"],
                nom=column["nom"],
                name_latin=column["latin"],
            )
            if created:
                species.save()
