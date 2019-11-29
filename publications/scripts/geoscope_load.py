from publications import models

import os
import logging

logging.basicConfig(level=logging.DEBUG, filename="geoScope_load.log", filemode="w")

FILE_PREFIX = "file:///"


def load_data(geoscope_name, file_path):
    # I'm making the asumption that all polygon files will have the same format
    # data[3] - FEATURESEQ - sequence number / point order
    # data[4] - XP - Longitude
    # data[5] - YP - Latitude

    geo_name = geoscope_name.upper()
    if models.GeographicScope.objects.filter(name=geo_name):
        logging.debug(geoscope_name + ": \n\t" + file_path)
    else:
        return

    file = open(file_path, "r")
    first = True

    for line in file:
        if first:
            first = False
            continue

        data = line.strip().split(',')

        if not models.Polygon.objects.filter(geoscope=models.GeographicScope.objects.get(name=geo_name), order=data[3]):
            geo = models.GeographicScope.objects.get(name=geo_name)
            models.Polygon(geoscope=geo, order=data[3], latitude=data[5], longitude=data[4]).save()


def load_scope(file_name):
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\data\\" + file_name

    file = open(file_path, "r")
    first = True
    for line in file:
        if first:
            first = False
            continue

        try:
            data = line.strip()
            if data:
                data = data.split(',')
                if data[1].startswith(FILE_PREFIX):
                    csv_file = data[1].replace(FILE_PREFIX, "")
                    try:
                        load_data(data[0], csv_file)
                    except:
                        logging.error("Error loading file: " + csv_file)

        except IndexError:
            logging.error("Could not load '" + line.strip() + "'")


def load():
    load_scope("GeographicScope_table.csv")


load()