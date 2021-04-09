from django.contrib import admin

# Register your models here.
from vault.models import Region, Purpose, Certainty, IndividualIdentification, ObservationSighting, OriginalMediafile

admin.site.register(Region)
admin.site.register(Purpose)
admin.site.register(Certainty)
admin.site.register(IndividualIdentification)
admin.site.register(ObservationSighting)
admin.site.register(OriginalMediafile)
