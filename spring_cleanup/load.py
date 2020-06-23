import os
from django.contrib.gis.utils import LayerMapping
from .models import Route

mapping = {
    'id': 'id',
    'description_en': 'descr',
    'recommended_people': 'no_ppl',
    'polygon': 'MULTIPOLYGON',
}

world_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'cleanup_routes.shp'),
)

def run(verbose=True):
    lm = LayerMapping(Route, world_shp, mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
