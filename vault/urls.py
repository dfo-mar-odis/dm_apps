
from . import views

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from .views import profile_upload

urlpatterns = [
    path('', views.index, name="index"),

    # path('admin/', admin.site.urls),
    # path('upload-csv/', profile_upload, name="profile_upload")
#     # SPECIES #
#     ###########
    path('species_list/', views.SpeciesListView.as_view(), name="species_list"),
#     # path('species/new/', views.SpeciesCreateView.as_view(), name="species_new"),
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),
#     # path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),
#     # path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),
    path('item_list/', views.ItemsListView.as_view(), name="item_list"),
    path('item_detail/<int:pk>/view/', views.ItemsDetailView.as_view(), name="item_detail")
    #

    # # PREDATORS #
    # #############
    # path('predators/', views.PredatorFilterView.as_view(), name="predator_filter"),
    # path('predator/new/', views.PredatorCreateView.as_view(), name="predator_new"),
    # path('predator/new/cruise/<int:cruise>/', views.PredatorCreateView.as_view(), name="predator_new"),
    # path('predator/<int:pk>/view/', views.PredatorDetailView.as_view(), name="predator_detail"),
    # path('predator/<int:pk>/edit/', views.PredatorUpdateView.as_view(), name="predator_edit"),
    # path('predator/<int:pk>/delete/', views.PredatorDeleteView.as_view(), name="predator_delete"),
    #
    # # PREY #
    # ########
    # path('predator/<int:predator>/species/<int:species>/add/', views.PreyCreateView.as_view(), name="prey_new"),
    # path('prey/<int:pk>/edit/', views.PreyUpdateView.as_view(), name="prey_edit"),
    # path('prey/<int:pk>/delete/', views.prey_delete, name="prey_delete"),
    #
    # # CRUISES #
    # ###########
    # path('cruises/', views.CruiseListView.as_view(), name ="cruise_list" ),
    # path('cruise/new/', views.CruiseCreateView.as_view(), name ="cruise_new" ),
    # path('cruise/<int:pk>/view/', views.CruiseDetailView.as_view(), name ="cruise_detail" ),
    # path('cruise/<int:pk>/edit/', views.CruiseUpdateView.as_view(), name ="cruise_edit" ),
    # path('cruise/<int:pk>/delete/', views.CruiseDeleteView.as_view(), name ="cruise_delete" ),
    #
    # # DIGESTION LEVELS #
    # ####################
    # path('digestion-levels/', views.DigestionListView.as_view(), name ="digestion_list" ),
    # path('digestion-level/new/', views.DigestionCreateView.as_view(), name ="digestion_new" ),
    # path('digestion-level/<int:pk>/edit/', views.DigestionUpdateView.as_view(), name ="digestion_edit" ),
    # path('digestion-level/<int:pk>/delete/', views.DigestionDeleteView.as_view(), name ="digestion_delete" ),
    #
    # # SAMPLERS #
    # ############
    # path('samplers/', views.SamplerListView.as_view(), name="sampler_list"),
    # path('sampler/new/', views.SamplerCreateView.as_view(), name="sampler_new"),
    # path('sampler/<int:pk>/edit/', views.SamplerUpdateView.as_view(), name="sampler_edit"),
    # path('sampler/<int:pk>/delete/', views.SamplerDeleteView.as_view(), name="sampler_delete"),
    #
    # # REPORT #
    # ###################
    # path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    # path('progress-report/', views.PreySummaryListView.as_view(), name="prey_summary_list"),
    # path('progress-report/<str:year>/export', views.export_prey_summary, name="export_prey_summary"),
    # path('reports/export-data/<str:year>/<str:cruise>/<str:spp>/', views.export_data_report, name="export_data_report"),
    #
]

app_name = 'vault'
