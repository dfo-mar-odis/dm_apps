from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

    # reference tables
    path('settings/filtration-types/', views.FiltrationTypeFormsetView.as_view(), name="manage_filtration_types"),  # tested
    path('settings/filtration-type/<int:pk>/delete/', views.FiltrationTypeHardDeleteView.as_view(), name="delete_filtration_type"),  # tested
    path('settings/dna-extraction-protocols/', views.DNAExtractionProtocolFormsetView.as_view(), name="manage_dna_extraction_protocols"),  # tested
    path('settings/dna-extraction-protocol/<int:pk>/delete/', views.DNAExtractionProtocolHardDeleteView.as_view(), name="delete_dna_extraction_protocol"),
    # tested
    path('settings/tags/', views.TagFormsetView.as_view(), name="manage_tags"),  # tested
    path('settings/tag/<int:pk>/delete/', views.TagHardDeleteView.as_view(), name="delete_tag"),  # tested

    # species
    path('species/', views.SpeciesListView.as_view(), name="species_list"),  # tested
    path('species/new/', views.SpeciesCreateView.as_view(), name="species_new"),  # tested
    path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),  # tested
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),  # tested
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),  # tested

    # collections
    path('collections/', views.CollectionListView.as_view(), name="collection_list"),  # tested
    path('collections/new/', views.CollectionCreateView.as_view(), name="collection_new"),  # tested
    path('collections/<int:pk>/edit/', views.CollectionUpdateView.as_view(), name="collection_edit"),  # tested
    path('collections/<int:pk>/delete/', views.CollectionDeleteView.as_view(), name="collection_delete"),  # tested
    path('collections/<int:pk>/view/', views.CollectionDetailView.as_view(), name="collection_detail"),  # tested
    path('collections/<int:pk>/import-samples/', views.ImportSamplesView.as_view(), name="import_samples"),

    # files
    path('collections/<int:collection>/new-file/', views.FileCreateView.as_view(), name='file_new'),  # tested
    path('files/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),  # tested
    path('files/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),  # tested

    # samples
    path('collections/<int:collection>/new-sample/', views.SampleCreateView.as_view(), name="sample_new"),  # tested
    path('samples/<int:pk>/edit/', views.SampleUpdateView.as_view(), name="sample_edit"),  # tested
    path('samples/<int:pk>/delete/', views.SampleDeleteView.as_view(), name="sample_delete"),  # tested
    path('samples/<int:pk>/view/', views.SampleDetailView.as_view(), name="sample_detail"),  # tested

    # filtration batches
    path('filtrations/', views.FiltrationBatchListView.as_view(), name="filtration_batch_list"),  # tested
    path('filtrations/new/', views.FiltrationBatchCreateView.as_view(), name="filtration_batch_new"),  # tested
    path('filtrations/<int:pk>/edit/', views.FiltrationBatchUpdateView.as_view(), name="filtration_batch_edit"),  # tested
    path('filtrations/<int:pk>/delete/', views.FiltrationBatchDeleteView.as_view(), name="filtration_batch_delete"),  # tested
    path('filtrations/<int:pk>/view/', views.FiltrationBatchDetailView.as_view(), name="filtration_batch_detail"),  # tested

    # extraction batches
    path('extractions/', views.ExtractionBatchListView.as_view(), name="extraction_batch_list"),  # tested
    path('extractions/new/', views.ExtractionBatchCreateView.as_view(), name="extraction_batch_new"),  # tested
    path('extractions/<int:pk>/edit/', views.ExtractionBatchUpdateView.as_view(), name="extraction_batch_edit"),  # tested
    path('extractions/<int:pk>/delete/', views.ExtractionBatchDeleteView.as_view(), name="extraction_batch_delete"),  # tested
    path('extractions/<int:pk>/view/', views.ExtractionBatchDetailView.as_view(), name="extraction_batch_detail"),  # tested

    # pcr batches
    path('pcrs/', views.PCRBatchListView.as_view(), name="pcr_batch_list"),  # tested
    path('pcrs/new/', views.PCRBatchCreateView.as_view(), name="pcr_batch_new"),  # tested
    path('pcrs/<int:pk>/edit/', views.PCRBatchUpdateView.as_view(), name="pcr_batch_edit"),  # tested
    path('pcrs/<int:pk>/delete/', views.PCRBatchDeleteView.as_view(), name="pcr_batch_delete"),  # tested
    path('pcrs/<int:pk>/view/', views.PCRBatchDetailView.as_view(), name="pcr_batch_detail"),  # tested

    # reports
    path('reports/', views.ReportSearchFormView.as_view(), name="reports"),  # tested

]

app_name = 'edna'
