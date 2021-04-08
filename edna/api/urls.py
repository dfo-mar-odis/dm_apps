from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'filters', views.FilterViewSet)
router.register(r'extracts', views.DNAExtractViewSet)
router.register(r'pcrs', views.PCRViewSet)
router.register(r'observations', views.SpeciesObservationViewSet)

urlpatterns = [
    path("edna/", include(router.urls)),  # tested
    path("edna/user/", views.CurrentUserAPIView.as_view(), name="edna-current-user"),

    path("edna/meta/models/filter/", views.FilterModelMetaAPIView.as_view(), name="edna-filter-model-meta"),
    path("edna/meta/models/extract/", views.DNAExtractModelMetaAPIView.as_view(), name="edna-extract-model-meta"),
    path("edna/meta/models/pcr/", views.PCRModelMetaAPIView.as_view(), name="edna-pcr-model-meta"),
    path("edna/meta/models/species-observation/", views.SpeciesObservationModelMetaAPIView.as_view(), name="edna-pcr-model-meta"),

]
