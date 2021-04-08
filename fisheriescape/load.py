# To use this file:
# python manage.py shell
# from fisheriescape import load
# load.run()
# exit()

import os
from django.contrib.gis.utils import LayerMapping
from .models import FisheryArea

# For NAFO.shp
mapping = {
    'layer_id': 'Layer_id',
    'name': 'ZONE',
    'polygon': 'MULTIPOLYGON',
}

nafo_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'NAFO_Atlantic.shp'),
)


def run(verbose=True):
    lm = LayerMapping(FisheryArea, nafo_shp, mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


# For SnowCrab_polygons.shp
# mapping = {
#     'layer_id': 'Layer_id',
#     'name': 'ZONE_1',
#     'polygon': 'MULTIPOLYGON',
# }
#
# crab_shp = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), 'data', 'SnowCrab_polygons.shp'),
# )
#
#
# def run(verbose=True):
#     lm = LayerMapping(FisheryArea, crab_shp, mapping, transform=False)
#     lm.save(strict=True, verbose=verbose)

## For Lobster_polygons.shp
# mapping = {
#     'layer_id': 'Layer_id',
#     'name': 'LFA',
#     'polygon': 'MULTIPOLYGON',
# }
#
# lobster_shp = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), 'data', 'Lobster_polygons.shp'),
# )
#
#
# def run(verbose=True):
#     lm = LayerMapping(FisheryArea, lobster_shp, mapping, transform=False)
#     lm.save(strict=True, verbose=verbose)
