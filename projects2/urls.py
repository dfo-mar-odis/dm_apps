from django.urls import path

from . import views

app_name = 'projects2'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

    # PROJECTS #
    ############

    path('projects/new/', views.ProjectCreateView.as_view(), name="project_new"),  # tested
    path('projects/<int:pk>/view/', views.ProjectDetailView.as_view(), name="project_detail"),  # tested
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name="project_edit"),  # tested
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name="project_delete"),  # tested
    path('projects/<int:pk>/clone/', views.ProjectCloneView.as_view(), name="project_clone"),  # tested
    path('projects/<int:pk>/references/', views.ProjectReferencesDetailView.as_view(), name="project_references"),  # tested

    path('my-list/', views.MyProjectListView.as_view(), name="my_project_list"),  # tested
    path('projects/explore/', views.ExploreProjectsTemplateView.as_view(), name="explore_projects"),  # tested
    path('projects/manage/', views.ManageProjectsTemplateView.as_view(), name="manage_projects"),  # tested

    # PROJECT YEAR #
    ################
    path('projects/<int:project>/new-project-year/', views.ProjectYearCreateView.as_view(), name="year_new"),  # tested
    path('project-years/<int:pk>/edit/', views.ProjectYearUpdateView.as_view(), name="year_edit"),  # tested
    path('project-years/<int:pk>/delete/', views.ProjectYearDeleteView.as_view(), name="year_delete"),  # tested
    path('project-years/<int:pk>/clone/', views.ProjectYearCloneView.as_view(), name="year_clone"),  # tested

    # STATUS REPORT #
    #################
    path('status-reports/<int:pk>/view/', views.StatusReportDetailView.as_view(), name="report_detail"),  # tested
    path('status-reports/<int:pk>/edit/', views.StatusReportUpdateView.as_view(), name="report_edit"),  # tested
    path('status-reports/<int:pk>/review/', views.StatusReportReviewUpdateView.as_view(), name="report_review"),  # tested
    path('status-reports/<int:pk>/delete/', views.StatusReportDeleteView.as_view(), name="report_delete"),  # tested
    path('status-reports/<int:pk>/print/', views.StatusReportPrintDetailView.as_view(), name="report_pdf"),  # tested

    # SETTINGS #
    ############
    # formsets
    path('settings/funding-sources/', views.FundingSourceFormsetView.as_view(), name="manage_funding_sources"),  # tested
    path('settings/funding-source/<int:pk>/delete/', views.FundingSourceHardDeleteView.as_view(), name="delete_funding_source"),  # tested

    path('settings/activity-types/', views.ActivityTypeFormsetView.as_view(), name="manage_activity_types"),  # tested
    path('settings/activity-type/<int:pk>/delete/', views.ActivityTypeHardDeleteView.as_view(), name="delete_activity_type"),  # tested

    path('settings/om-categories/', views.OMCategoryFormsetView.as_view(), name="manage_om_cats"),  # tested
    path('settings/om-category/<int:pk>/delete/', views.OMCategoryHardDeleteView.as_view(), name="delete_om_cat"),  # tested

    path('settings/employee-types/', views.EmployeeTypeFormsetView.as_view(), name="manage_employee_types"),  # tested
    path('settings/employee-type/<int:pk>/delete/', views.EmployeeTypeHardDeleteView.as_view(), name="delete_employee_type"),  # tested

    path('settings/tags/', views.TagFormsetView.as_view(), name="manage_tags"),  # tested
    path('settings/tag/<int:pk>/delete/', views.TagHardDeleteView.as_view(), name="delete_tag"),  # tested

    path('settings/help-texts/', views.HelpTextFormsetView.as_view(), name="manage_help_text"),  # tested
    path('settings/help-text/<int:pk>/delete/', views.HelpTextHardDeleteView.as_view(), name="delete_help_text"),  # tested

    path('settings/levels/', views.LevelFormsetView.as_view(), name="manage_levels"),  # tested
    path('settings/level/<int:pk>/delete/', views.LevelHardDeleteView.as_view(), name="delete_level"),  # tested

    path('settings/themes/', views.ThemeFormsetView.as_view(), name="manage_themes"),  # tested
    path('settings/theme/<int:pk>/delete/', views.ThemeHardDeleteView.as_view(), name="delete_theme"),  # tested

    path('settings/upcoming-dates/', views.UpcomingDateFormsetView.as_view(), name="manage-upcoming-dates"),  # tested
    path('settings/upcoming-date/<int:pk>/delete/', views.UpcomingDateHardDeleteView.as_view(), name="delete-upcoming-date"),  # tested

    path('settings/csrf-themes/', views.CSRFThemeFormsetView.as_view(), name="manage_csrf_themes"), # tested
    path('settings/csrf-theme/<int:pk>/delete/', views.CSRFThemeHardDeleteView.as_view(), name="delete_csrf_theme"),# tested

    path('settings/csrf-sub-themes/', views.CSRFSubThemeFormsetView.as_view(), name="manage_csrf_sub_themes"),# tested
    path('settings/csrf-sub-theme/<int:pk>/delete/', views.CSRFSubThemeHardDeleteView.as_view(), name="delete_csrf_sub_theme"),# tested

    path('settings/csrf-priorities/', views.CSRFPriorityFormsetView.as_view(), name="manage_csrf_priorities"),# tested
    path('settings/csrf-prioritie/<int:pk>/delete/', views.CSRFPriorityHardDeleteView.as_view(), name="delete_csrf_priority"),# tested

    path('settings/csrf-client-information/', views.CSRFClientInformationFormsetView.as_view(), name="manage_csrf_client_information"),# tested
    path('settings/csrf-client-information/<int:pk>/delete/', views.CSRFClientInformationHardDeleteView.as_view(), name="delete_csrf_client_information"),# tested


    # full
    path('settings/reference-materials/', views.ReferenceMaterialListView.as_view(), name="ref_mat_list"),   # tested
    path('settings/reference-materials/new/', views.ReferenceMaterialCreateView.as_view(), name="ref_mat_new"),  # tested
    path('settings/reference-materials/<int:pk>/edit/', views.ReferenceMaterialUpdateView.as_view(), name="ref_mat_edit"),  # tested
    path('settings/reference-materials/<int:pk>/delete/', views.ReferenceMaterialDeleteView.as_view(), name="ref_mat_delete"),  # tested

    path('settings/functional-groups/', views.FunctionalGroupListView.as_view(), name="group_list"),  # tested
    path('settings/functional-groups/new/', views.FunctionalGroupCreateView.as_view(), name="group_new"),  # tested
    path('settings/functional-groups/<int:pk>/edit/', views.FunctionalGroupUpdateView.as_view(), name="group_edit"),  # tested
    path('settings/functional-groups/<int:pk>/delete/', views.FunctionalGroupDeleteView.as_view(), name="group_delete"),  # tested

    # admin
    path('admin/staff-list/', views.AdminStaffListView.as_view(), name="admin_staff_list"), # tested
    path('admin/staff/<int:pk>/edit/<str:qry>/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"), # tested
    path('admin/staff/<int:pk>/edit/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"), # tested


    # Reports #
    ###########
    path('reports/', views.ReportSearchFormView.as_view(), name="reports"), # tested
    path('reports/science-culture-committee-report/', views.culture_committee_report, name="culture_committee_report"),# tested
    path('reports/csrf-submission-list/', views.export_csrf_submission_list, name="export_csrf_submission_list"),# tested
    path('reports/project-status-summary/', views.project_status_summary, name="export_project_status_summary"),# tested
    path('reports/project-list/', views.export_project_list, name="export_project_list"),  # TODO: test
    path('reports/sar-workplan/', views.export_sar_workplan, name="export_sar_workplan"),
    path('reports/regional-staff-allocation/', views.export_regional_staff_allocation, name="export_rsa"),
    path('reports/project-position-allocation/', views.export_project_position_allocation, name="export_ppa"),  # TODO: test

    #special
    path('projects/<int:pk>/acrdp-application/', views.export_acrdp_application, name="export_acrdp_application"),
    path('projects/<int:pk>/acrdp-budget/', views.export_acrdp_budget, name="export_acrdp_budget"),
    path('projects/<int:pk>/csrf-application/', views.csrf_application, name="csrf_application"),
    path('projects/<int:pk>/sara-application/', views.sara_application, name="sara_application"),

    # Admin Users
    path('settings/users/', views.UserListView.as_view(), name='user_list'),
    path('settings/user/<int:pk>/toggle/<str:type>/', views.toggle_user, name='toggle_user'),


]
