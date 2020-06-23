import os

from azure.storage.blob import BlockBlobService

from django.core import serializers
from django.core.files import File
import uuid
from .import models

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


#
#
def get_file(request, file):
    my_file = models.File.objects.get(pk=file)
    blob_name = my_file.file

    if settings.AZURE_STORAGE_ACCOUNT_NAME:
        AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
        token_credential = MSIAuthentication(resource=f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net')
        blobService = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential)
        blobService.create_blob_from_path()
        blob_file = blobService.get_blob_to_bytes("media", blob_name)
        response = HttpResponse(blob_file.content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{blob_name}"'
    else:
        response = HttpResponse(my_file.file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{blob_name}"'

    return response




def upload_mediafiles_to_blob():
    block_blob_service = BlockBlobService(account_name='dmappsdev', account_key='')
    container_name ='media'

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR = os.path.join(BASE_DIR, 'media', 'travel')

    for files in os.listdir(MEDIA_DIR):
        block_blob_service.create_blob_from_path(container_name,files,os.path.join(local_path,files))

