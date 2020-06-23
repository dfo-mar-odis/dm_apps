from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'grais'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.IndexView.as_view(), name="index"),
    path('dataflow/', views.DataFlowTemplateView.as_view(), name="dataflow"),

    # SAMPLE #
    ##########
    path('sample/list/', views.SampleListView.as_view(), name="sample_list"),
    path('sample/new/', views.SampleCreateView.as_view(), name="sample_new"),
    path('sample/<int:pk>/view/', views.SampleDetailView.as_view(), name="sample_detail"),
    path('sample/<int:pk>/edit/', views.SampleUpdateView.as_view(), name="sample_edit"),
    path('sample/<int:pk>/delete/', views.SampleDeleteView.as_view(), name="sample_delete"),

    # STATION #
    ###########
    path('station/', views.StationListView.as_view(), name="station_list"),
    path('station/new/', views.StationCreateView.as_view(), name="station_create"),
    path('station/<int:pk>/view/', views.StationDetailView.as_view(), name="station_detail"),
    path('station/<int:pk>/edit/', views.StationUpdateView.as_view(), name="station_edit"),
    path('station/<int:pk>/delete/', views.StationDeleteView.as_view(), name="station_delete"),

    # SAMPLE NOTE #
    #############
    path('sample/<int:sample>/sample-note/new/', views.SampleNoteCreateView.as_view(), name="sample_note_new"),
    path('sample-note/<int:pk>/edit/', views.SampleNoteUpdateView.as_view(), name="sample_note_edit"),
    path('sample-note/<int:pk>/delete/', views.sample_note_delete, name="sample_note_delete"),

    # SPECIES #
    ###########
    path('species/', views.SpeciesListView.as_view(), name="species_list"),
    path('species/new/', views.SpeciesCreateView.as_view(), name="species_create"),
    path('new-species-to-surface-<int:surface>/', views.SpeciesCreatePopoutView.as_view(), name="species_add"),
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),
    path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),

    # PROBE MEASUREMENT #
    #####################
    path('sample/<int:sample>/probe-data/new/', views.ProbeMeasurementCreateView.as_view(),
         name="probe_measurement_new"),
    path('probe-data/<int:pk>/view/', views.ProbeMeasurementDetailView.as_view(), name="probe_measurement_detail"),
    path('probe-data/<int:pk>/edit/', views.ProbeMeasurementUpdateView.as_view(), name="probe_measurement_edit"),
    path('probe-data/<int:pk>/delete/', views.ProbeMeasurementDeleteView.as_view(), name="probe_measurement_delete"),

    # LINE #
    ########
    path('sample/<int:sample>/line/new/', views.LineCreateView.as_view(), name="line_new"),
    path('line/<int:pk>/view/', views.LineDetailView.as_view(), name="line_detail"),
    path('line/<int:pk>/edit/', views.LineUpdateView.as_view(), name="line_edit"),
    path('line/<int:pk>/delete/', views.LineDeleteView.as_view(), name="line_delete"),

    # SURFACE #
    ###########
    path('line/<int:line>/surface/new/', views.SurfaceCreateView.as_view(), name="surface_new"),
    path('surface/<int:pk>/view/', views.SurfaceDetailView.as_view(), name="surface_detail"),
    path('surface/<int:pk>/edit/', views.SurfaceUpdateView.as_view(), name="surface_edit"),
    path('surface/<int:pk>/delete/', views.SurfaceDeleteView.as_view(), name="surface_delete"),

    # SPECIES OBSERVATIONS (for sample + line level obs) #
    ########################################################
    path('species-observation/<str:type>/<int:pk>/insert/', views.SpeciesObservationInsertView.as_view(),
         name="spp_obs_insert"),
    path('species-observation/<str:type>/<int:pk>/new-spp/<int:species>/',
         views.SpeciesObservationCreatePopoutView.as_view(), name="spp_obs_new_pop"),
    path('species-observation/<str:type>/obs-pk/<int:pk>/edit/', views.SpeciesObservationUpdatePopoutView.as_view(),
         name="spp_obs_edit_pop"),
    # path('surface-species/<int:pk>/view/', views.SurfaceSpeciesDetailPopoutView.as_view(), name ="surface_spp_detail_pop" ),
    path('species-observation/<str:type>/obs-pk/<int:pk>/delete/return-to-<str:backto>/',
         views.species_observation_delete, name="spp_obs_delete"),

    # SURFACE SPECIES #
    ###################
    path('surface/<int:surface>/species/insert/', views.SurfacaeSpeciesInsertView.as_view(), name="surface_spp_insert"),
    path('surface/<int:surface>/species/<int:species>/new-surface-species/',
         views.SurfaceSpeciesCreatePopoutView.as_view(), name="surface_spp_new_pop"),
    path('surface-species/<int:pk>/edit/', views.SurfaceSpeciesUpdatePopoutView.as_view(), name="surface_spp_edit_pop"),
    # path('surface-species/<int:pk>/view/', views.SurfaceSpeciesDetailPopoutView.as_view(), name ="surface_spp_detail_pop" ),
    path('surface-species/<int:pk>/delete/return-to-<str:backto>/', views.surface_species_delete,
         name="surface_spp_delete"),

    path('person/new/', views.PersonCreateView.as_view(), name="person_create"),
    path('person/<int:pk>/view/', views.PersonDetailView.as_view(), name="person_detail"),
    path('person/<int:pk>/edit/', views.PersonUpdateView.as_view(), name="person_edit"),

    # INCIDENTAL REPORT #
    #####################
    path('incidental-report/list/', views.ReportListView.as_view(), name="report_list"),
    path('incidental-report/new/', views.ReportCreateView.as_view(), name="report_new"),
    path('incidental-report/<int:pk>/view/', views.ReportDetailView.as_view(), name="report_detail"),
    path('incidental-report/<int:pk>/edit/', views.ReportUpdateView.as_view(), name="report_edit"),
    path('incidental-report/<int:pk>/delete/', views.ReportDeleteView.as_view(), name="report_delete"),
    path('incidental-report/<int:report>/species/<int:species>/delete/', views.report_species_observation_delete,
         name="report_species_delete"),
    path('incidental-report/<int:report>/species/<int:species>/add/', views.report_species_observation_add, name="report_species_add"),

    # FOLLOWUP #
    ############
    path('report/<int:report>/follow-up/new/', views.FollowUpCreateView.as_view(), name="follow_up_new"),
    path('follow-up/<int:pk>/edit/', views.FollowUpUpdateView.as_view(), name="follow_up_edit"),
    path('follow-up/<int:pk>/delete/', views.follow_up_delete, name="follow_up_delete"),

    # ESTUARY #
    ###########
    path('estuaries/', views.EstuaryListView.as_view(), name="estuary_list"),
    path('estuary/new/', views.EstuaryCreateView.as_view(), name="estuary_new"),
    path('estuary/<int:pk>/view/', views.EstuaryDetailView.as_view(), name="estuary_detail"),
    path('estuary/<int:pk>/edit/', views.EstuaryUpdateView.as_view(), name="estuary_edit"),
    path('estuary/<int:pk>/delete/', views.EstuaryDeleteView.as_view(), name="estuary_delete"),

    # SITE #
    ###########
    path('estuary/<int:estuary>/new/site/', views.SiteCreateView.as_view(), name="site_new"),
    # path('site/new/', views.NoEstuarySiteCreateView.as_view(), name="site_new"),
    path('site/<int:pk>/view/', views.SiteDetailView.as_view(), name="site_detail"),
    path('site/<int:pk>/edit/', views.SiteUpdateView.as_view(), name="site_edit"),
    path('site/<int:pk>/delete/', views.SiteDeleteView.as_view(), name="site_delete"),

    # GC SAMPLE #
    ##########
    path('green-crab-samples/', views.GCSampleListView.as_view(), name="gcsample_list"),
    path('green-crab-sample/new/', views.GCSampleCreateView.as_view(), name="gcsample_new"),
    path('green-crab-sample/<int:pk>/view/', views.GCSampleDetailView.as_view(), name="gcsample_detail"),
    path('green-crab-sample/<int:pk>/edit/', views.GCSampleUpdateView.as_view(), name="gcsample_edit"),
    path('green-crab-sample/<int:pk>/delete/', views.GCSampleDeleteView.as_view(), name="gcsample_delete"),

    # PROBE MEASUREMENT #
    #####################
    path('green-crab-sample/<int:gcsample>/gc-probe-data/new/', views.GCProbeMeasurementCreateView.as_view(),
         name="gcprobe_measurement_new"),
    path('gc-probe-data/<int:pk>/view/', views.GCProbeMeasurementDetailView.as_view(), name="gcprobe_measurement_detail"),
    path('gc-probe-data/<int:pk>/edit/', views.GCProbeMeasurementUpdateView.as_view(), name="gcprobe_measurement_edit"),
    path('gc-probe-data/<int:pk>/delete/', views.GCProbeMeasurementDeleteView.as_view(), name="gcprobe_measurement_delete"),

    # TRAP #
    ########
    path('green-crab-sample/<int:gcsample>/trap/new/', views.TrapCreateView.as_view(), name="trap_new"),
    path('trap/<int:pk>/view/', views.TrapDetailView.as_view(), name="trap_detail"),
    path('trap/<int:pk>/edit/', views.TrapUpdateView.as_view(), name="trap_edit"),
    path('trap/<int:pk>/delete/', views.TrapDeleteView.as_view(), name="trap_delete"),

    # path('bycatch/<int:pk>/delete/', views.bycatch_delete, name="bycatch_delete"),
    # path('trap/<int:trap>/crab/<int:species>/add/', views.report_species_observation_add, name="crab_add"),
    # path('trap/<int:trap>/bycatch/<int:species>/add/', views.report_species_observation_add, name="bycatch_add"),

    # CATCH #
    ########
    path('catch/<int:trap>/species/<int:species>/new/', views.CatchCreateViewPopout.as_view(), name="catch_new"),
    path('catch/<int:pk>/edit/', views.CatchUpdateViewPopout.as_view(), name="catch_edit"),
    path('catch/<int:pk>/delete/', views.catch_delete, name="catch_delete"),
    path('trap/<int:trap>/manage-catch/type/<str:type>/', views.manage_catch, name="manage_catch"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/species-by-sample-spreadsheet/<str:species_list>/', views.species_sample_spreadsheet_export,
         name="spp_sample_xlsx"),
    path('reports/opendata1/<int:year>/', views.export_open_data_ver1, name="od1_report"),
    path('reports/opendata1/', views.export_open_data_ver1, name="od1_report"),
    path('reports/opendata1/dictionary/', views.export_open_data_ver1_dictionary, name="od1_dictionary"),
    path('reports/opendata1/wms/<str:year>/lang/<int:lang>/', views.export_open_data_ver1_wms, name="od1_wms"),
    # GC monitoring
    path('reports/gc/<int:year>/cpue/', views.export_gc_cpue, name="gc_cpue_report"),
    path('reports/gc/<int:year>/envr/', views.export_gc_envr, name="gc_envr_report"),
    path('reports/gc/site-list/', views.export_gc_sites, name="gc_site_report"),

]
