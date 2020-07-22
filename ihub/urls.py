from django.urls import path
from . import views

app_name = 'ihub'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
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
    path('entry/<int:entry>/note/new/', views.NoteCreateView.as_view(), name="note_new"),# TESTED
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name="note_edit"),# TESTED
    path('note/<int:pk>/delete/', views.note_delete, name="note_delete"),# TESTED

    # ENTRYPERSON #
    ###############
    path('entry/<int:entry>/person/new/', views.EntryPersonCreateView.as_view(), name="ep_new"),# TESTED
    path('dfo-person/<int:pk>/edit/', views.EntryPersonUpdateView.as_view(), name="ep_edit"),# TESTED
    path('dfo-person/<int:pk>/delete/', views.entry_person_delete, name="ep_delete"),# TESTED

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
    path('settings/sectors/', views.manage_sectors, name="manage_sectors"),
    path('settings/organizations/', views.manage_orgs, name="manage_orgs"),
    path('settings/status/', views.manage_statuses, name="manage_statuses"),
    path('settings/entry-types/', views.manage_entry_types, name="manage_entry_types"),
    path('settings/funding-purpose/', views.manage_funding_purposes, name="manage_funding_purposes"),
    path('settings/reserves/', views.manage_reserves, name="manage_reserves"),
    path('settings/nations/', views.manage_nations, name="manage_nations"),
    path('settings/funding-programs/', views.manage_programs, name="manage_programs"),
    path('settings/relationship-ratings/', views.manage_ratings, name="manage_ratings"),

    path('settings/relationship-rating/<int:pk>/delete/', views.delete_rating, name="delete_rating"),
    path('settings/status/<int:pk>/delete/', views.delete_status, name="delete_status"),
    path('settings/entry-type/<int:pk>/delete/', views.delete_entry_type, name="delete_entry_type"),
    path('settings/funding-purpose/<int:pk>/delete/', views.delete_funding_purpose, name="delete_funding_purpose"),
    path('settings/reserve/<int:pk>/delete/', views.delete_reserve, name="delete_reserve"),
    path('settings/nation/<int:pk>/delete/', views.delete_nation, name="delete_nation"),
    path('settings/funding-program/<int:pk>/delete/', views.delete_program, name="delete_program"),
    path('settings/users/', views.UserListView.as_view(), name='user_list'),
    path('settings/users/ihub/<int:ihub>/', views.UserListView.as_view(), name='user_list'),
    path('settings/user/<int:pk>/toggle/<str:type>/', views.toggle_user, name='toggle_user'),
    # path('settings/user/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
]
