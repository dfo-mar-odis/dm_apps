from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sample-species', views.SampleSpeciesViewSet)
router.register(r'line-species', views.LineSpeciesViewSet)
router.register(r'surface-species', views.SurfaceSpeciesViewSet)
# router.register(r'extracts', views.DNAExtractViewSet)
# router.register(r'pcrs', views.PCRViewSet)
# router.register(r'observations', views.SpeciesObservationViewSet)

urlpatterns = [
    path("grais/", include(router.urls)),  # tested
    path("grais/user/", views.CurrentUserAPIView.as_view(), name="grais-current-user"),


    path("grais/meta/models/species/", views.SpeciesModelMetaAPIView.as_view(), name="grais-species-model-meta"),

    # path("grais/meta/models/extract/", views.DNAExtractModelMetaAPIView.as_view(), name="edna-extract-model-meta"),
    # path("grais/meta/models/pcr/", views.PCRModelMetaAPIView.as_view(), name="edna-pcr-model-meta"),
    # path("grais/meta/models/species-observation/", views.SpeciesObservationModelMetaAPIView.as_view(), name="edna-pcr-model-meta"),

]
