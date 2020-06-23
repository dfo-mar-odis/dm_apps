from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'inventory'

urlpatterns = [

    # RESOURCE #
    ############
    path('', views.Index.as_view(), name="index"),
    path('list/', views.ResourceListView.as_view(), name="resource_list"),
    path('my-list/', views.MyResourceListView.as_view(), name="my_resource_list"),
    path('<int:pk>/view/', views.ResourceDetailView.as_view(), name="resource_detail"),
    path('<int:pk>/pdf/', views.ResourceDetailPDFView.as_view(), name="resource_pdf"),
    path('<int:pk>/full-view/', views.ResourceFullDetailView.as_view(), name="resource_full_detail"),
    path('<int:pk>/edit/', views.ResourceUpdateView.as_view(), name="resource_edit"),
    path('<int:pk>/delete/', views.ResourceDeleteView.as_view(), name="resource_delete"),
    path('new/', views.ResourceCreateView.as_view(), name="resource_new"),
    path('<int:pk>/flag-for-deletion/', views.ResourceDeleteFlagUpdateView.as_view(), name="resource_flag_delete"),
    path('<int:pk>/flag-for-publication/', views.ResourcePublicationFlagUpdateView.as_view(), name="resource_flag_publication"),

    # Open Data
    path('open-data-dashboard/', views.OpenDataDashboardTemplateView.as_view(), name="open_data_dashboard"),


    # RESOURCE PERSON #
    ###################
    path('<int:resource>/insert-person/', views.ResourcePersonFilterView.as_view(), name="resource_person_filter"),
    path('<int:resource>/person/<int:person>/add/', views.ResourcePersonCreateView.as_view(), name="resource_person_add"),
    path('resource-person/<int:pk>/delete/', views.ResourcePersonDeleteView.as_view(), name="resource_person_delete"),
    path('resource-person/<int:pk>/edit/', views.ResourcePersonUpdateView.as_view(), name="resource_person_edit"),

    # PEOPLE #
    ##########

    # **** DJF: I think these urls, views and templates can be deleted.

    path('<int:resource>/insert-person/new/', views.PersonCreateView.as_view(), name="person_add"),
    path('insert-person/new/', views.PersonCreateViewPopout.as_view(), name="person_add_popout"),
    path('<int:resource>/person/<int:person>/edit/', views.PersonUpdateView.as_view(), name="person_edit"),
    path('person/<int:person>/edit/', views.PersonUpdateView.as_view(), name="person_edit"),

    # RESOURCE KEYWORD #
    ####################
    path('<int:pk>/insert-keyword/', views.ResourceKeywordUpdateView.as_view(), name="resource_keyword_edit"),
    path('<int:resource>/insert-keyword/', views.ResourceKeywordFilterView.as_view(), name="resource_keyword_filter"),
    path('<int:resource>/insert-topic-category/', views.ResourceTopicCategoryFilterView.as_view(), name="resource_topic_category_filter"),
    path('<int:resource>/insert-core-subject/', views.ResourceCoreSubjectFilterView.as_view(), name="resource_core_subject_filter"),
    path('<int:resource>/insert-species/', views.ResourceSpeciesFilterView.as_view(), name="resource_species_filter"),
    path('<int:resource>/insert-location/', views.ResourceLocationFilterView.as_view(), name="resource_location_filter"),
    path('<int:resource>/keyword/<int:keyword>/add-<slug:keyword_type>/', views.resource_keyword_add, name="resource_keyword_add"),
    path('<int:resource>/keyword/<int:keyword>/add/', views.resource_keyword_add, name="resource_keyword_add"),
    path('<int:resource>/keyword/<int:keyword>/remove/', views.resource_keyword_delete, name="resource_keyword_delete"),

    # KEYWORD #
    ###########
    path('<int:resource>/keyword/<int:pk>/view/', views.KeywordDetailView.as_view(), name="keyword_detail"),
    path('<int:resource>/keyword/<int:pk>/edit/', views.KeywordUpdateView.as_view(), name="keyword_edit"),
    path('<int:resource>/keyword/<int:keyword>/delete/', views.keyword_delete, name="keyword_delete"),
    path('<int:resource>/keyword/new/', views.KeywordCreateView.as_view(), name="keyword_new"),

    # RESOURCE CITATION #
    #####################
    path('<int:resource>/insert-citation/', views.ResourceCitationFilterView.as_view(), name="resource_citation_filter"),
    path('<int:resource>/citation/<int:citation>/add-citation/', views.resource_citation_add, name="resource_citation_add"),
    path('<int:resource>/citation/<int:citation>/remove/', views.resource_citation_delete, name="resource_citation_delete"),

    # CITATION #
    ############
    path('<int:resource>/citation/<int:pk>/view/', views.CitationDetailView.as_view(), name="citation_detail"),
    path('<int:resource>/citation/<int:pk>/edit/', views.CitationUpdateView.as_view(), name="citation_edit"),
    path('<int:resource>/citation/<int:citation>/delete/', views.citation_delete, name="citation_delete"),
    path('<int:resource>/citation/new/', views.CitationCreateView.as_view(), name="citation_new"),

    # PUBLICATION #
    ###############
    path('publication/new/', views.PublicationCreateView.as_view(), name="publication_new"),

    # XML GOODNESS #
    ################
    path('<int:resource>/xml/export/publish-<slug:publish>/', views.export_resource_xml, name="export_xml"),

    # DATA MANAGEMENT ADMIN #
    #########################
    path('dm-admin/', views.DataManagementHomeTemplateView.as_view(), name="dm_home"),
    path('dm-admin/custodian-list/', views.DataManagementCustodianListView.as_view(), name="dm_custodian_list"),
    path('dm-admin/custodian/<int:pk>/detail/', views.DataManagementCustodianDetailView.as_view(), name="dm_custodian_detail"),
    path('dm-admin/custodian/<int:person>/send-request-for-certification/', views.send_certification_request,
         name="send_certification_email"),
    path('dm-admin/custodian/<int:person>/', views.CustodianPersonUpdateView.as_view(), name="dm_person_edit"),
    path('dm-admin/published-resource-list/', views.PublishedResourcesListView.as_view(), name="dm_published_list"),
    path('dm-admin/flagged/<str:flag_type>/', views.FlaggedListView.as_view(), name="dm_flagged_list"),
    path('dm-admin/certifications/', views.CertificationListView.as_view(), name="dm_certification_list"),
    path('dm-admin/modifications/', views.ModificationListView.as_view(), name="dm_modification_list"),

    ## SECTIONS
    path('my-section/', views.MySectionDetailView.as_view(), name="my_section_detail"),
    path('dm-admin/sections/list/', views.SectionListView.as_view(), name="dm_section_list"),
    path('dm-admin/sections/detail/<int:pk>/', views.SectionDetailView.as_view(), name="dm_section_detail"),
    # path('dm-admin/sections/edit/<int:pk>/', views.SectionUpdateView.as_view(), name="dm_section_edit"),
    # path('dm-admin/sections/delete/<int:pk>/', views.SectionDeleteView.as_view(), name="dm_section_delete"),
    # path('dm-admin/sections/new/', views.SectionCreateView.as_view(), name="dm_section_new"),
    path('dm-admin/sections/<int:section>/send-section-report/', views.send_section_report, name="send_section_report_email"),

    # RESOURCE CERTIFICATION #
    ##########################
    path('resource/<int:pk>/certify/', views.ResourceCertificationCreateView.as_view(), name="resource_certify"),
    path('remove-certification/<int:pk>/', views.ResourceCertificationDeleteView.as_view(), name="resource_certification_delete"),

    # FILES #
    #########
    path('resource/<int:resource>/file/new/', views.FileCreateView.as_view(), name='file_create'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # DATA RESOURCE #
    #################
    path('resource/<int:resource>/data-resource/new/', views.DataResourceCreateView.as_view(), name='data_resource_create'),
    path('data-resource/<int:pk>/edit/', views.DataResourceUpdateView.as_view(), name='data_resource_edit'),
    path('data-resource/<int:pk>/delete/', views.DataResourceDeleteView.as_view(), name='data_resource_delete'),
    path('data-resource/<int:pk>/clone/', views.data_resource_clone, name='data_resource_clone'),

    # WEB SERVICES #
    #################
    path('resource/<int:resource>/web-service/new/', views.WebServiceCreateView.as_view(),
         name='web_service_create'),
    path('web-service/<int:pk>/edit/', views.WebServiceUpdateView.as_view(), name='web_service_edit'),
    path('web-service/<int:pk>/delete/', views.WebServiceDeleteView.as_view(), name='web_service_delete'),
    path('web-service/<int:pk>/clone/', views.web_service_clone, name='web_service_clone'),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/export-batch-xml/<str:sections>/', views.export_batch_xml, name="export_batch_xml"),
    path('reports/odi-report/', views.export_odi_report, name="export_odi_report"),


    # TEMP #
    ########

    #  this was used to walk over program to programs
    path('metadata-formset/section/<int:section>/', views.temp_formset, name="formset"),
    # path('project-program-list/', views.MyTempListView.as_view(), name="my_list"),
    # path('reports/capacity-report/fy/<str:fy>/orgs/<str:orgs>/', views.capacity_export_spreadsheet, name="capacity_xlsx"),
    # path('reports/capacity-report/', views.capacity_export_spreadsheet, name="capacity_xlsx"),
    # path('reports/capacity-report/fy/<str:fy>/', views.capacity_export_spreadsheet, name="capacity_xlsx"),
    # path('reports/capacity-report/orgs/<str:orgs>/', views.capacity_export_spreadsheet, name="capacity_xlsx"),
    # path('reports/cue-card/org/<int:org>/', views.OrganizationCueCard.as_view(), name="report_q"),

]
