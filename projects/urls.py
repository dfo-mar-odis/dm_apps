from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'projects'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.IndexTemplateView.as_view(), name="index"),

    # PROJECTS #
    ############
    path('my-list/', views.MyProjectListView.as_view(), name="my_project_list"),
    path('all/', views.ProjectListView.as_view(), name="project_list"),
    path('new/', views.ProjectCreateView.as_view(), name="project_new"),
    path('<int:pk>/view/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project/<int:pk>/print/', views.ProjectPrintDetailView.as_view(), name="project_print"),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name="project_edit"),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name="project_delete"),
    path('project/<int:pk>/delete/popout/<int:pop>/', views.ProjectDeleteView.as_view(), name="project_delete"),
    path('project/<int:pk>/submit/', views.ProjectSubmitUpdateView.as_view(), name="project_submit"),
    path('project/<int:pk>/submit/popout/<int:pop>/', views.ProjectSubmitUpdateView.as_view(), name="project_submit"),
    path('project/<int:pk>/notes/', views.ProjectNotesUpdateView.as_view(), name="project_notes"),
    path('project/<int:pk>/clone/', views.ProjectCloneUpdateView.as_view(), name="project_clone"),
    # path('approval/project/<int:pk>/', views.ProjectApprovalUpdateView.as_view(), name="project_approve"),
    path('recommendation/project/<int:pk>/', views.ProjectRecommendationUpdateView.as_view(), name="project_recommend"),

    # From management views
    ################
    # the following 3 should be deleted once fully phased out
    path('my-section/', views.MySectionListView.as_view(), name="my_section_list"),
    #
    path('section/<int:section>/', views.SectionListView.as_view(), name="section_project_list"),
    path('project/<int:pk>/overview/', views.ProjectOverviewDetailView.as_view(), name="project_overview"),
    path('project/<int:pk>/overview/popout/<int:pop>/', views.ProjectOverviewDetailView.as_view(), name="project_overview"),

    # STAFF #
    #########
    path('project/<int:project>/staff/new/', views.StaffCreateView.as_view(), name="staff_new"),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name="staff_edit"),
    path('staff/<int:pk>/delete/', views.staff_delete, name="staff_delete"),
    path('staff/<int:pk>/overtime-calculator/', views.OverTimeCalculatorTemplateView.as_view(), name="ot_calc"),

    #  this was used to walk over program to programs
    path('project-formset/region/<int:region>/fy/<int:fy>/', views.temp_formset, name="formset"),
    path('project-formset/region/<int:region>/fy/<int:fy>/section/<str:section_str>/', views.temp_formset, name="formset"),
    path('project-program-list/', views.MyTempListView.as_view(), name="my_list"),

    # USER #
    ########
    path('user/new/', views.UserCreateView.as_view(), name="user_new"),

    # Collaborator #
    ################
    path('project/<int:project>/collaborator/new/', views.CollaboratorCreateView.as_view(), name="collab_new"),
    path('collaborator/<int:pk>/edit/', views.CollaboratorUpdateView.as_view(), name="collab_edit"),
    path('collaborator/<int:pk>/delete/', views.collaborator_delete, name="collab_delete"),

    # Collaborative Agreements #
    ############################
    path('project/<int:project>/agreement/new/', views.AgreementCreateView.as_view(), name="agreement_new"),
    path('agreement/<int:pk>/edit/', views.AgreementUpdateView.as_view(), name="agreement_edit"),
    path('agreement/<int:pk>/delete/', views.agreement_delete, name="agreement_delete"),

    # O&M COST #
    ############
    path('project/<int:project>/om-cost/new/', views.OMCostCreateView.as_view(), name="om_new"),
    path('om-cost/<int:pk>/edit/', views.OMCostUpdateView.as_view(), name="om_edit"),
    path('om-cost/<int:pk>/delete/', views.om_cost_delete, name="om_delete"),
    path('om-cost/<int:project>/clear-empty/', views.om_cost_clear, name="om_clear"),
    path('om-cost/<int:project>/populate-all/', views.om_cost_populate, name="om_populate"),

    # CAPITAL COST #
    ################
    path('project/<int:project>/capital-cost/new/', views.CapitalCostCreateView.as_view(), name="capital_new"),
    path('capital-cost/<int:pk>/edit/', views.CapitalCostUpdateView.as_view(), name="capital_edit"),
    path('capital-cost/<int:pk>/delete/', views.capital_cost_delete, name="capital_delete"),

    # G&C COST #
    ############
    path('project/<int:project>/gc-cost/new/', views.GCCostCreateView.as_view(), name="gc_new"),
    path('gc-cost/<int:pk>/edit/', views.GCCostUpdateView.as_view(), name="gc_edit"),
    path('gc-cost/<int:pk>/delete/', views.gc_cost_delete, name="gc_delete"),

    # FILES #
    #########
    path('project/<int:project>/file/new/', views.FileCreateView.as_view(), name='file_new'),
    path('project/<int:project>/file/new/status-report/<int:status_report>/', views.FileCreateView.as_view(), name='file_new'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # STATUS REPORT #
    #################
    path('project/<int:project>/status-report/new/', views.StatusReportCreateView.as_view(), name="report_new"),
    path('status-report/<int:pk>/edit/', views.StatusReportUpdateView.as_view(), name="report_edit"),
    path('status-report/<int:pk>/delete/', views.StatusReportDeleteView.as_view(), name="report_delete"),
    path('status-report/<int:pk>/pdf/', views.StatusReportPrintDetailView.as_view(), name="report_print"),

    # MILESTONE #
    #############
    path('project/<int:project>/milestone/new/', views.MilestoneCreateView.as_view(), name="milestone_new"),
    path('milestone/<int:pk>/edit/', views.MilestoneUpdateView.as_view(), name="milestone_edit"),
    path('milestone/<int:pk>/delete/', views.milestone_delete, name="milestone_delete"),

    # MILESTONE UPDATE #
    ####################
    path('milestone-update/<int:pk>/edit/', views.MilestoneUpdateUpdateView.as_view(), name="milestone_update_edit"),

    # FUNCTIONAL GROUP #
    ####################
    path('functional-groups/', views.FunctionalGroupListView.as_view(), name="group_list"),
    path('functional-group/new/', views.FunctionalGroupCreateView.as_view(), name="group_new"),
    path('functional-group/<int:pk>/edit/', views.FunctionalGroupUpdateView.as_view(), name="group_edit"),
    path('functional-group/<int:pk>/delete/', views.FunctionalGroupDeleteView.as_view(), name="group_delete"),
    path('functional-group/<int:pk>/view/', views.FunctionalGroupDetailView.as_view(), name="group_detail"),

    # SETTINGS #
    ############
    path('settings/funding-sources/', views.FundingSourceFormsetView.as_view(), name="manage_funding_sources"),
    path('settings/funding-source/<int:pk>/delete/', views.FundingSourceHardDeleteView.as_view(), name="delete_funding_source"),

    path('settings/activity-types/', views.ActivityTypeFormsetView.as_view(), name="manage_activity_types"),
    path('settings/activity-type/<int:pk>/delete/', views.ActivityTypeHardDeleteView.as_view(), name="delete_activity_type"),

    path('settings/om-categories/', views.OMCategoryFormsetView.as_view(), name="manage_om_cats"),
    path('settings/om-category/<int:pk>/delete/', views.OMCategoryHardDeleteView.as_view(), name="delete_om_cat"),

    path('settings/employee-types/', views.EmployeeTypeFormsetView.as_view(), name="manage_employee_types"),
    path('settings/employee-type/<int:pk>/delete/', views.EmployeeTypeHardDeleteView.as_view(), name="delete_employee_type"),

    path('settings/statuses/', views.StatusFormsetView.as_view(), name="manage_statuses"),
    path('settings/status/<int:pk>/delete/', views.StatusHardDeleteView.as_view(), name="delete_status"),

    path('settings/tags/', views.TagFormsetView.as_view(), name="manage_tags"),
    path('settings/tag/<int:pk>/delete/', views.TagHardDeleteView.as_view(), name="delete_tag"),

    path('settings/help-texts/', views.HelpTextFormsetView.as_view(), name="manage_help_text"),
    path('settings/help-text/<int:pk>/delete/', views.HelpTextHardDeleteView.as_view(), name="delete_help_text"),

    path('settings/levels/', views.LevelFormsetView.as_view(), name="manage_levels"),
    path('settings/level/<int:pk>/delete/', views.LevelHardDeleteView.as_view(), name="delete_level"),

    path('settings/programs/', views.ProgramFormsetView.as_view(), name="manage_programs"),
    path('settings/program/<int:pk>/delete/', views.ProgramHardDeleteView.as_view(), name="delete_program"),

    path('settings/themes/', views.ThemeFormsetView.as_view(), name="manage_themes"),
    path('settings/theme/<int:pk>/delete/', views.ThemeHardDeleteView.as_view(), name="delete_theme"),

    path('settings/upcoming-dates/', views.UpcomingDateFormsetView.as_view(), name="manage-upcoming-dates"),
    path('settings/upcoming-date/<int:pk>/delete/', views.UpcomingDateHardDeleteView.as_view(), name="delete-upcoming-date"),

    path('admin/staff-list/', views.AdminStaffListView.as_view(), name="admin_staff_list"),
    path('admin/project-program-list/', views.AdminProjectProgramListView.as_view(), name="admin_project_program_list"),
    path('admin/project-program/<int:pk>/edit/<str:qry>/', views.AdminProjectProgramUpdateView.as_view(), name="admin_pp_edit"),
    path('admin/project-program/<int:pk>/edit/', views.AdminProjectProgramUpdateView.as_view(), name="admin_pp_edit"),

    path('admin/staff/<int:pk>/edit/<str:qry>/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"),
    path('admin/staff/<int:pk>/edit/', views.AdminStaffUpdateView.as_view(), name="admin_staff_edit"),

    path('admin/submitted-unapproved-list/', views.SubmittedUnapprovedProjectsListView.as_view(), name="admin_submitted_unapproved"),

    # project approvals
    path('admin/project-approvals/search/', views.ProjectApprovalsSearchView.as_view(), name="admin_project_approval_search"),
    path('admin/project-approval-for/region/<int:region>/fiscal-year/<int:fy>/', views.ProjectApprovalFormsetView.as_view(), name="admin_project_approval"),


    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path(
        'reports/master-spreadsheet/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
        views.master_spreadsheet, name="report_master"),
    path('reports/project-summary/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFProjectSummaryReport.as_view(), name="pdf_project_summary"),
    path(
        'reports/batch-workplan-export/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
        views.PDFProjectPrintoutReport.as_view(), name="pdf_printout"),

    # this is a special view of the masterlist report that is called from the my_section view
    path('reports/section-head-spreadsheet/fiscal-year/<int:fiscal_year>/user/<int:user>', views.master_spreadsheet, name="report_sh"),

    path('reports/export-program-list/', views.export_program_list, name="export_program_list"),

    # GULF REGION REPORTS
    path('reports/FTE_summary/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFFTESummaryReport.as_view(), name="pdf_fte_summary"),
    path('reports/OT/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFOTSummaryReport.as_view(), name="pdf_ot"),
    path('reports/costs/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFCostSummaryReport.as_view(), name="pdf_costs"),
    path('reports/collaborators/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFCollaboratorReport.as_view(), name="pdf_collab"),
    path('reports/agreements/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFAgreementsReport.as_view(), name="pdf_agreements"),
    path('reports/dougs-report/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.dougs_spreadsheet, name="doug_report"),
    path('reports/feedback/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFFeedbackReport.as_view(), name="pdf_feedback"),
    path('reports/data-management/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.PDFDataReport.as_view(), name="pdf_data"),
    path('reports/sara-report/fiscal-year/<int:fiscal_year>/funding/<int:funding>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>',
         views.PDFFundingReport.as_view(), name="pdf_funding"),
    path('reports/sara-report/fiscal-year/<int:fiscal_year>/funding/<int:funding>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.funding_spreadsheet, name="xls_funding"),
    path('reports/sara-report/fiscal-year/<int:fiscal_year>/funding/<int:funding>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/omcatagory/<str:omcatagory>/',
         views.funding_spreadsheet, name="xls_funding_by_om"),
    path('reports/covid/fiscal-year/<int:fiscal_year>/regions/<str:regions>/divisions/<str:divisions>/sections/<str:sections>/',
         views.covid_spreadsheet, name="xls_covid"),
    # path('reports/workplan-summary/fiscal-year/<int:fiscal_year>', views.workplan_summary, name="workplan_summary"),

    # INTERACTIVE WORKPLANS #
    #########################
    path('interactive-workplan/region/<int:region>/division/<int:division>/section/<int:section>/year/<int:fiscal_year>/type/<str:type>/', views.IWGroupList.as_view(),
         name="iw_group_list"),

    # by section / program by fgroup
    path('interactive-workplan/<int:fiscal_year>/region/<int:region>/division/<int:division>/section/<int:section>/small-item/<int:small_item>/group/<int:group>/projects/type/<str:type>/',
         views.IWProjectList.as_view(), name="iw_project_list"),
    # by section / program
    path('interactive-workplan/<int:fiscal_year>/region/<int:region>/division/<int:division>/section/<int:section>/small-item/<int:small_item>/projects/type/<str:type>/',
         views.IWProjectList.as_view(), name="iw_project_list"),

    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name="note_edit"),

]