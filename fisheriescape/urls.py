from django.urls import path
from . import views

from django.contrib.gis import admin

app_name = "fisheriescape"

urlpatterns = [
    path('admin', admin.site.urls),
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.index, name="index"),

    # MAP #
    path('map/', views.MapView.as_view(), name="map_view"),

    # SPECIES #

    path('species-list/', views.SpeciesListView.as_view(), name="species_list"),
    path('species/new/', views.SpeciesCreateView.as_view(), name="species_new"),
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),
    path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),

    # FISHERY AREA #

    path('fisheryarea-list/', views.FisheryAreaListView.as_view(), name="fishery_area_list"),
    # path('fisheryarea/new/', views.FisheryAreaCreateView.as_view(), name="fishery_area_new"),
    path('fisheryarea/<int:pk>/view/', views.FisheryAreaDetailView.as_view(), name="fishery_area_detail"),
    # path('fisheryarea/<int:pk>/edit/', views.FisheryAreaUpdateView.as_view(), name="fishery_area_edit"),
    # path('fisheryarea/<int:pk>/delete/', views.FisheryAreaDeleteView.as_view(), name="fishery_area_delete"),

    # FISHERY #

    path('fishery-list/', views.FisheryListView.as_view(), name="fishery_list"),
    path('fishery/new/', views.FisheryCreateView.as_view(), name="fishery_new"),
    path('fishery/<int:pk>/view/', views.FisheryDetailView.as_view(), name="fishery_detail"),
    path('fishery/<int:pk>/edit/', views.FisheryUpdateView.as_view(), name="fishery_edit"),
    path('fishery/<int:pk>/delete/', views.FisheryDeleteView.as_view(), name="fishery_delete"),

]
