from django.urls import path

from .views import biofouling_views, shared_views, ir_views

app_name = 'grais'

urlpatterns = [

    # SETTINGS
    path('', shared_views.IndexView.as_view(), name="index"),

    path('settings/probes/', shared_views.ProbeFormsetView.as_view(), name="manage_probes"),
    path('settings/probe/<int:pk>/delete/', shared_views.ProbeHardDeleteView.as_view(), name="delete_probe"),
    path('settings/samplers/', shared_views.SamplerFormsetView.as_view(), name="manage_samplers"),
    path('settings/sampler/<int:pk>/delete/', shared_views.SamplerHardDeleteView.as_view(), name="delete_sampler"),

    # species
    path('species/', shared_views.SpeciesListView.as_view(), name="species_list"),
    path('species/new/', shared_views.SpeciesCreateView.as_view(), name="species_new"),
    path('species/<int:pk>/edit/', shared_views.SpeciesUpdateView.as_view(), name="species_edit"),
    path('species/<int:pk>/delete/', shared_views.SpeciesDeleteView.as_view(), name="species_delete"),
    path('species/<int:pk>/view/', shared_views.SpeciesDetailView.as_view(), name="species_detail"),

    # station #
    ###########
    path('stations/', biofouling_views.StationListView.as_view(), name="station_list"),
    path('stations/new/', biofouling_views.StationCreateView.as_view(), name="station_new"),
    path('stations/<int:pk>/view/', biofouling_views.StationDetailView.as_view(), name="station_detail"),
    path('stations/<int:pk>/edit/', biofouling_views.StationUpdateView.as_view(), name="station_edit"),
    path('stations/<int:pk>/delete/', biofouling_views.StationDeleteView.as_view(), name="station_delete"),

    # sample #
    ##########
    path('samples/', biofouling_views.SampleListView.as_view(), name="sample_list"),
    path('samples/new/', biofouling_views.SampleCreateView.as_view(), name="sample_new"),
    path('samples/<int:pk>/view/', biofouling_views.SampleDetailView.as_view(), name="sample_detail"),
    path('samples/<int:pk>/edit/', biofouling_views.SampleUpdateView.as_view(), name="sample_edit"),
    path('samples/<int:pk>/delete/', biofouling_views.SampleDeleteView.as_view(), name="sample_delete"),

    # sample note #
    ###############
    path('samples/<int:sample>/new-note/', biofouling_views.SampleNoteCreateView.as_view(), name="sample_note_new"),
    path('sample-notes/<int:pk>/edit/', biofouling_views.SampleNoteUpdateView.as_view(), name="sample_note_edit"),
    path('sample-notes/<int:pk>/delete/', biofouling_views.SampleNoteDeleteView.as_view(), name="sample_note_delete"),

    # probe measurements #
    ######################
    path('samples/<int:sample>/new-measurement/', biofouling_views.ProbeMeasurementCreateView.as_view(), name="measurement_new"),
    path('measurements/<int:pk>/edit/', biofouling_views.ProbeMeasurementUpdateView.as_view(), name="measurement_edit"),
    path('measurements/<int:pk>/delete/', biofouling_views.ProbeMeasurementDeleteView.as_view(), name="measurement_delete"),

    # species observations #
    ########################
    path('<str:type>/<int:pk>/observations/', biofouling_views.SpeciesObservationTemplateView.as_view(), name="species_observations"),

    # LINE #
    ########
    path('samples/<int:sample>/new-line/', biofouling_views.LineCreateView.as_view(), name="line_new"),
    path('lines/<int:pk>/view/', biofouling_views.LineDetailView.as_view(), name="line_detail"),
    path('lines/<int:pk>/edit/', biofouling_views.LineUpdateView.as_view(), name="line_edit"),
    path('lines/<int:pk>/delete/', biofouling_views.LineDeleteView.as_view(), name="line_delete"),

    # SURFACE #
    ###########
    path('lines/<int:line>/new-surface/', biofouling_views.SurfaceCreateView.as_view(), name="surface_new"),
    path('surfaces/<int:pk>/view/', biofouling_views.SurfaceDetailView.as_view(), name="surface_detail"),
    path('surfaces/<int:pk>/edit/', biofouling_views.SurfaceUpdateView.as_view(), name="surface_edit"),
    path('surfaces/<int:pk>/delete/', biofouling_views.SurfaceDeleteView.as_view(), name="surface_delete"),

    # INCIDENTAL REPORT #
    #####################
    path('incidental-reports/', ir_views.ReportListView.as_view(), name="ir_list"),
    path('incidental-reports/new/', ir_views.ReportCreateView.as_view(), name="ir_new"),
    path('incidental-reports/<int:pk>/view/', ir_views.ReportDetailView.as_view(), name="ir_detail"),
    path('incidental-reports/<int:pk>/edit/', ir_views.ReportUpdateView.as_view(), name="ir_edit"),
    path('incidental-reports/<int:pk>/delete/', ir_views.ReportDeleteView.as_view(), name="ir_delete"),
    # path('incidental-reports/<int:report>/species/<int:species>/delete/', ir_views.ir_species_observation_delete, name="ir_species_delete"),
    # path('incidental-reports/<int:report>/species/<int:species>/add/', ir_views.ir_species_observation_add, name="ir_species_add"),

    # FOLLOWUP #
    ############
    path('report/<int:report>/follow-up/new/', ir_views.FollowUpCreateView.as_view(), name="follow_up_new"),
    path('follow-up/<int:pk>/edit/', ir_views.FollowUpUpdateView.as_view(), name="follow_up_edit"),
    path('follow-up/<int:pk>/delete/', ir_views.follow_up_delete, name="follow_up_delete"),
    #
    # # ESTUARY #
    # ###########
    # path('estuaries/', views.EstuaryListView.as_view(), name="estuary_list"),
    # path('estuary/new/', views.EstuaryCreateView.as_view(), name="estuary_new"),
    # path('estuary/<int:pk>/view/', views.EstuaryDetailView.as_view(), name="estuary_detail"),
    # path('estuary/<int:pk>/edit/', views.EstuaryUpdateView.as_view(), name="estuary_edit"),
    # path('estuary/<int:pk>/delete/', views.EstuaryDeleteView.as_view(), name="estuary_delete"),
    #
    # # SITE #
    # ###########
    # path('estuary/<int:estuary>/new/site/', views.SiteCreateView.as_view(), name="site_new"),
    # # path('site/new/', views.NoEstuarySiteCreateView.as_view(), name="site_new"),
    # path('site/<int:pk>/view/', views.SiteDetailView.as_view(), name="site_detail"),
    # path('site/<int:pk>/edit/', views.SiteUpdateView.as_view(), name="site_edit"),
    # path('site/<int:pk>/delete/', views.SiteDeleteView.as_view(), name="site_delete"),
    #
    # # GC SAMPLE #
    # ##########
    # path('green-crab-samples/', views.GCSampleListView.as_view(), name="gcsample_list"),
    # path('green-crab-sample/new/', views.GCSampleCreateView.as_view(), name="gcsample_new"),
    # path('green-crab-sample/<int:pk>/view/', views.GCSampleDetailView.as_view(), name="gcsample_detail"),
    # path('green-crab-sample/<int:pk>/edit/', views.GCSampleUpdateView.as_view(), name="gcsample_edit"),
    # path('green-crab-sample/<int:pk>/delete/', views.GCSampleDeleteView.as_view(), name="gcsample_delete"),
    #
    # # PROBE MEASUREMENT #
    # #####################
    # path('green-crab-sample/<int:gcsample>/gc-probe-data/new/', views.GCProbeMeasurementCreateView.as_view(),
    #      name="gcprobe_measurement_new"),
    # path('gc-probe-data/<int:pk>/view/', views.GCProbeMeasurementDetailView.as_view(), name="gcprobe_measurement_detail"),
    # path('gc-probe-data/<int:pk>/edit/', views.GCProbeMeasurementUpdateView.as_view(), name="gcprobe_measurement_edit"),
    # path('gc-probe-data/<int:pk>/delete/', views.GCProbeMeasurementDeleteView.as_view(), name="gcprobe_measurement_delete"),
    #
    # # TRAP #
    # ########
    # path('green-crab-sample/<int:gcsample>/trap/new/', views.TrapCreateView.as_view(), name="trap_new"),
    # path('trap/<int:pk>/view/', views.TrapDetailView.as_view(), name="trap_detail"),
    # path('trap/<int:pk>/edit/', views.TrapUpdateView.as_view(), name="trap_edit"),
    # path('trap/<int:pk>/delete/', views.TrapDeleteView.as_view(), name="trap_delete"),
    #
    # # path('bycatch/<int:pk>/delete/', views.bycatch_delete, name="bycatch_delete"),
    # # path('trap/<int:trap>/crab/<int:species>/add/', views.report_species_observation_add, name="crab_add"),
    # # path('trap/<int:trap>/bycatch/<int:species>/add/', views.report_species_observation_add, name="bycatch_add"),
    #
    # # CATCH #
    # ########
    # path('catch/<int:trap>/species/<int:species>/new/', views.CatchCreateViewPopout.as_view(), name="catch_new"),
    # path('catch/<int:pk>/edit/', views.CatchUpdateViewPopout.as_view(), name="catch_edit"),
    # path('catch/<int:pk>/delete/', views.catch_delete, name="catch_delete"),
    # path('trap/<int:trap>/manage-catch/type/<str:type>/', views.manage_catch, name="manage_catch"),
    #
    # # Reports #
    # ###########
    path('reports/search/', shared_views.ReportSearchFormView.as_view(), name="reports"),
    # path('reports/species-by-sample-spreadsheet/<str:species_list>/', views.species_sample_spreadsheet_export,
    #      name="spp_sample_xlsx"),
    # path('reports/biofouling-presence-absence/', views.biofouling_presence_absence_spreadsheet_export, name="biofouling_pa_xlsx"),
    # path('reports/opendata1/<int:year>/', views.export_open_data_ver1, name="od1_report"),
    # path('reports/opendata1/', views.export_open_data_ver1, name="od1_report"),
    # path('reports/opendata1/dictionary/', views.export_open_data_ver1_dictionary, name="od1_dictionary"),
    # path('reports/opendata1/wms/<str:year>/lang/<int:lang>/', views.export_open_data_ver1_wms, name="od1_wms"),
    # # GC monitoring
    # path('reports/gc/<int:year>/cpue/', views.export_gc_cpue, name="gc_cpue_report"),
    # path('reports/gc/<int:year>/envr/', views.export_gc_envr, name="gc_envr_report"),
    # path('reports/gc/site-list/', views.export_gc_sites, name="gc_site_report"),
    #
    #

]
