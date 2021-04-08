import os

from django.conf import settings
from django.core import serializers
from django.core.files import File

from fisheriescape import models


# for individual exports, can use:
# python manage.py dumpdata app_name.model_name > fisheriescape/fixtures/file.json

#to run this script do:
# python manage.py shell
# from fisheriescape.scripts import export_fixtures
# export_fixtures()

def export_fixtures():
    """ a simple function to export the important lookup tables. These fixtures will be used for testing and also for seeding new instances"""
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    models_to_export = [
        models.FisheryArea,
        models.Species,
        models.MarineMammal,

    ]
    for model in models_to_export:
        data = serializers.serialize("json", model.objects.all())
        my_label = model._meta.db_table
        f = open(os.path.join(fixtures_dir, f'{my_label}.json'), 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()

