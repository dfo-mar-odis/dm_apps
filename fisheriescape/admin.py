from django.contrib.gis import admin
from .models import FisheryArea, MarineMammal

admin.site.register(FisheryArea, admin.GeoModelAdmin)
admin.site.register(MarineMammal, admin.ModelAdmin)
