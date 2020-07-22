from django.urls import path
from . import views

app_name = 'ihub'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),  # TESTED

    # PERSON #
    ##########
    path('people/', views.PersonListView.as_view(), name="person_list"),  # TESTED
    path('person/new/', views.PersonCreateView.as_view(), name="person_new"),  # TESTED
    path('person/new/popout/', views.PersonCreateViewPopout.as_view(), name="person_new_pop"),  # TESTED
    path('person/<int:pk>/view/', views.PersonDetailView.as_view(), name="person_detail"),  # TESTED
    path('person/<int:pk>/edit/', views.PersonUpdateView.as_view(), name="person_edit"),  # TESTED
    path('person/<int:pk>/edit/popout/', views.PersonUpdateViewPopout.as_view(), name="person_edit_pop"),  # TESTED
    path('person/<int:pk>/delete/', views.PersonDeleteView.as_view(), name="person_delete"),  # TESTED

    # ORGANIZATION #
    ################
    path('organizations/', views.OrganizationListView.as_view(), name="org_list"),  # TESTED
    path('organization/new/', views.OrganizationCreateView.as_view(), name="org_new"),  # TESTED
    path('organization/<int:pk>/view/', views.OrganizationDetailView.as_view(), name="org_detail"),  # TESTED
    path('organization/<int:pk>/edit/', views.OrganizationUpdateView.as_view(), name="org_edit"),  # TESTED
    path('organization/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name="org_delete"),  # TESTED

    # ORGANIZATIONPERSON #
    ######################
    path('organization/<int:org>/member/new/', views.MemberCreateView.as_view(), name="member_new"),  # TESTED
    path('member/<int:pk>/edit/', views.MemberUpdateView.as_view(), name="member_edit"),  # TESTED
    path('member/<int:pk>/delete/', views.MemberDeleteView.as_view(), name="member_delete"),  # TESTED
    # path('member/<int:pk>/delete/', views.member_delete, name="member_delete"),

    # # Entry #
    # #########
    path('entries/', views.EntryListView.as_view(), name="entry_list"),  # TESTED
    path('entry/new/', views.EntryCreateView.as_view(), name="entry_new"),  # TESTED
    path('entry/<int:pk>/view', views.EntryDetailView.as_view(), name="entry_detail"),  # TESTED
    path('entry/<int:pk>/edit', views.EntryUpdateView.as_view(), name="entry_edit"),  # TESTED
    path('entry/<int:pk>/delete', views.EntryDeleteView.as_view(), name="entry_delete"),  # TESTED

    # NOTES #
    #########
    path('entry/<int:entry>/note/new/', views.NoteCreateView.as_view(), name="note_new"),  # TESTED
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name="note_edit"),  # TESTED
    path('note/<int:pk>/delete/', views.note_delete, name="note_delete"),  # TESTED

    # ENTRYPERSON #
    ###############
    path('entry/<int:entry>/person/new/', views.EntryPersonCreateView.as_view(), name="ep_new"),  # TESTED
    path('dfo-person/<int:pk>/edit/', views.EntryPersonUpdateView.as_view(), name="ep_edit"),  # TESTED
    path('dfo-person/<int:pk>/delete/', views.entry_person_delete, name="ep_delete"),  # TESTED

    # Consultation Instructions #
    #############################
    path('organization/<int:org>/instructions/new/', views.InstructionCreateView.as_view(), name="instruction_new"),# TESTED
    path('instructions/<int:pk>/edit/', views.InstructionUpdateView.as_view(), name="instruction_edit"),# TESTED
    path('instructions/<int:pk>/delete/', views.InstructionDeleteView.as_view(), name="instruction_delete"),# TESTED

    # ConsultationRole (ie.. a member who is consulted ) #
    ##############
    path('organization/<int:organization>/member/<int:member>/new/', views.ConsultationRoleCreateView.as_view(), name="consultee_new"),
    path('consultee/<int:pk>/edit/', views.ConsultationRoleUpdateView.as_view(), name="consultee_edit"),
    path('consultee/<int:pk>/delete/', views.ConsultationRoleDeleteView.as_view(), name="consultee_delete"),

    # FILE #
    ########
    path('entry/<int:entry>/file/new/', views.FileCreateView.as_view(), name="file_new"),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name="file_edit"),
    path('file/<int:pk>/delete/', views.file_delete, name="file_delete"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/capacity-report/fy/<str:fy>/sectors/<str:sectors>/orgs/<str:orgs>/', views.capacity_export_spreadsheet,
         name="capacity_xlsx"),
    path('reports/cue-card/org/<int:org>/', views.OrganizationCueCard.as_view(), name="report_q"),
    path('reports/summary-report/fy/<str:fy>/sectors/<str:sectors>/orgs/<str:orgs>/', views.summary_export_spreadsheet,
         name="summary_xlsx"),
    path('reports/summary-report-pdf/fy/<str:fy>/sectors/<str:sectors>/orgs/<str:orgs>/', views.PDFSummaryReport.as_view(),
         name="summary_pdf"),
    path(
        'reports/consultation-log/fy/<str:fy>/orgs/<str:orgs>/statuses/<str:statuses>/entry-types/<str:entry_types>/report-title/<str:report_title>/',
        views.ConsultationLogPDFTemplateView.as_view(), name="consultation_log"),
    path(
        'reports/consultation-log/fy/<str:fy>/orgs/<str:orgs>/statuses/<str:statuses>/entry-types/<str:entry_types>/report-title/<str:report_title>/xlsx/',
        views.consultation_log_export_spreadsheet, name="consultation_log_xlsx"),

    # SETTINGS #
    ############

    path('settings/organizations/', views.OrganizationFormsetView.as_view(), name="manage_orgs"),  # TESTED


    path('settings/sectors/', views.SectorFormsetView.as_view(), name="manage_sectors"),  # TESTED
    path('settings/sector/<int:pk>/delete/', views.SectorHardDeleteView.as_view(), name="delete_sector"),  # TESTED

    path('settings/statuses/', views.StatusFormsetView.as_view(), name="manage_statuses"),  # TESTED
    path('settings/status/<int:pk>/delete/', views.StatusHardDeleteView.as_view(), name="delete_status"),  # TESTED

    path('settings/entry-types/', views.EntryTypeFormsetView.as_view(), name="manage_entry_types"),  # TESTED
    path('settings/entry-type/<int:pk>/delete/', views.EntryTypeHardDeleteView.as_view(), name="delete_entry_type"),  # TESTED

    path('settings/funding-purposes/', views.FundingPurposeFormsetView.as_view(), name="manage_funding_purposes"),  # TESTED
    path('settings/funding-purpose/<int:pk>/delete/', views.FundingPurposeHardDeleteView.as_view(), name="delete_funding_purpose"),  # TESTED

    path('settings/reserves/', views.ReserveFormsetView.as_view(), name="manage_reserves"),  # TESTED
    path('settings/reserve/<int:pk>/delete/', views.ReserveHardDeleteView.as_view(), name="delete_reserve"),  # TESTED

    path('settings/nations/', views.NationFormsetView.as_view(), name="manage_nations"),  # TESTED
    path('settings/nation/<int:pk>/delete/', views.NationHardDeleteView.as_view(), name="delete_nation"),  # TESTED

    path('settings/funding-programs/', views.FundingProgramFormsetView.as_view(), name="manage_programs"),  # TESTED
    path('settings/funding-program/<int:pk>/delete/', views.FundingProgramHardDeleteView.as_view(), name="delete_program"),  # TESTED

    path('settings/relationship-ratings/', views.RelationshipRatingFormsetView.as_view(), name="manage_ratings"),  # TESTED
    path('settings/relationship-rating/<int:pk>/delete/', views.RelationshipRatingHardDeleteView.as_view(), name="delete_rating"),  # TESTED


    path('settings/users/', views.UserListView.as_view(), name='user_list'),
    path('settings/users/ihub/<int:ihub>/', views.UserListView.as_view(), name='user_list'),
    path('settings/user/<int:pk>/toggle/<str:type>/', views.toggle_user, name='toggle_user'),
]
