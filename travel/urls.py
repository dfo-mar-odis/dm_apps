from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),
    path('util/conf_details', views.get_conf_details, name='conf_details'),

    # TRIP REQUEST #
    ################
    # path('requests/', views.TripRequestListView.as_view(), name="request_list"), # remove
    path('requests/<str:type>/', views.TripRequestListView.as_view(), name="request_list"),

    # path('your-requests/', views.TripRequestListView.as_view(), name="request_list"),

    path('request/new/<str:type>/', views.TripRequestCreateView.as_view(), name="request_new"),
    path('request/<int:parent_request>/new-child-request/', views.TripRequestCreateView.as_view(), name="request_new"),

    path('request/<int:pk>/view/from/<str:type>/', views.TripRequestDetailView.as_view(), name="request_detail"),
    path('request/<int:pk>/edit/from/<str:type>/', views.TripRequestUpdateView.as_view(), name="request_edit"),
    path('request/<int:pk>/delete/from/<str:type>/', views.TripRequestDeleteView.as_view(), name="request_delete"),
    path('request/<int:pk>/submit/from/<str:type>/', views.TripRequestSubmitUpdateView.as_view(), name="request_submit"),
    path('request/<int:pk>/clone/from/<str:type>/', views.TripRequestCloneUpdateView.as_view(), name="request_clone"),
    path('request/<int:pk>/cancel/from/<str:type>/', views.TripRequestCancelUpdateView.as_view(), name="request_cancel"),

    path('request/<int:pk>/print/', views.TravelPlanPDF.as_view(), name="request_print"),

    path('request/<int:pk>/clone-child/pop/<str:type>', views.ChildTripRequestCloneUpdateView.as_view(), name="child_request_clone"),

    path('request/<int:pk>/admin-notes/', views.TripRequestAdminNotesUpdateView.as_view(), name="admin_notes_edit"),

    # REVIEWER APPROVAL
    path('requests/review/', views.TripRequestReviewListView.as_view(), name="request_review_list"),
    path('requests/review/<str:which_ones>/', views.TripRequestReviewListView.as_view(), name="request_review_list"),
    # ADMIN APPROVAL LIST (FOR ADM and RDG)
    path('admin/approval/for/<str:type>/', views.TripRequestAdminApprovalListView.as_view(), name="admin_approval_list"),
    path('admin/approval/for/<str:type>/region/<int:region>/', views.TripRequestAdminApprovalListView.as_view(),
         name="admin_approval_list"),
    # path('admin/<int:pk>/approve/', views.TripRequestAdminApproveUpdateView.as_view(), name="admin_approve"),

    # this would be for a reviewer, recommender, approver
    path('review/<int:pk>/approve/', views.TripRequestReviewerUpdateView.as_view(), name="tr_review_update"),
    # This would be for an admin
    path('review/<int:pk>/approve/for/<str:type>/', views.TripRequestReviewerUpdateView.as_view(), name="tr_review_update"),
    path('adm-review/<int:pk>/<int:approve>/', views.TripRequestReviewerADMUpdateView.as_view(), name="tr_review_adm_update"),

    # TRIP REQUEST REVIEWERS
    path('request/<int:triprequest>/reset-reviewers/for/<str:type>/', views.reset_reviewers, name="reset_tr_reviewers"),
    path('request/<int:triprequest>/manage-reviewers/for/<str:type>/', views.manage_reviewers, name="manage_tr_reviewers"),
    path('trip-request-reviewer/<int:pk>/delete/', views.TripRequestReviewerHardDeleteView.as_view(), name="delete_tr_reviewer"),
    path('trip-request-reviewer/<int:pk>/skip/', views.SkipReviewerUpdateView.as_view(), name="skip_tr_reviewer"),

    # TRIP #
    ########
    # path('trips/', views.TripListView.as_view(), name="trip_list"),
    path('trips/<str:type>/', views.TripListView.as_view(), name="trip_list"),
    path('trip/new/<str:type>/', views.TripCreateView.as_view(), name="trip_new"),
    path('trip/<int:pk>/view/from/<str:type>/', views.TripDetailView.as_view(), name="trip_detail"),
    path('trip/<int:pk>/edit/from/<str:type>/', views.TripUpdateView.as_view(), name="trip_edit"),
    path('trip/<int:pk>/delete/from/<str:type>/', views.TripDeleteView.as_view(), name="trip_delete"),
    path('trip/<int:pk>/cancel/from/<str:type>/', views.TripCancelUpdateView.as_view(), name="trip_cancel"),

    # verification / other admin views
    path('trip/<int:pk>/admin-notes/', views.TripAdminNotesUpdateView.as_view(), name="trip_admin_notes_edit"),
    path('trip/<int:pk>/review-process/', views.TripReviewProcessUpdateView.as_view(), name="trip_review_toggle"),
    path('admin/trip-verification-list/region/<int:region>/adm/<int:adm>/', views.TripVerificationListView.as_view(),
         name="admin_trip_verification_list"),
    path('trip/<int:pk>/verify/region/<int:region>/adm/<int:adm>/', views.TripVerifyUpdateView.as_view(), name="trip_verify"),
    path('select-a-trip-to-reassign-requests-to/<int:pk>/', views.TripSelectFormView.as_view(), name="trip_reassign_select"),
    path('re-assign-requests-from-trip/<int:trip_a>/to/<int:trip_b>/', views.TripReassignConfirmView.as_view(),
         name="trip_reassign_confirm"),

    # TRIP REVIEWERS
    path('trip/<int:trip>/reset-reviewers/from/<str:type>/', views.reset_reviewers, name="reset_trip_reviewers"),
    path('trip/<int:trip>/manage-reviewers/from/<str:type>/', views.manage_reviewers, name="manage_trip_reviewers"),
    path('trip-reviewer/<int:pk>/delete/', views.TripReviewerHardDeleteView.as_view(), name="delete_trip_reviewer"),

    # REVIEWER APPROVAL
    path('trips-for-your-review/<str:which_ones>/', views.TripReviewListView.as_view(), name="trip_review_list"),
    path('tagged-trips/', views.TripReviewListView.as_view(), name="trip_review_list"),
    path('trip-reviewer/<int:pk>/review/', views.TripReviewerUpdateView.as_view(), name="trip_reviewer_update"),
    path('trip/<int:pk>/skip/', views.SkipTripReviewerUpdateView.as_view(), name="trip_skip"),

    # FILES #
    #########
    path('request/<int:trip_request>/file/new/', views.FileCreateView.as_view(), name='file_new'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # SETTINGS #
    ############
    path('settings/statuses/', views.StatusFormsetView.as_view(), name="manage_statuses"),
    # path('settings/status/<int:pk>/delete/', views.StatusHardDeleteView.as_view(), name="delete_status"),
    path('settings/help-text/', views.HelpTextFormsetView.as_view(), name="manage_help_text"),
    path('settings/help-text/<int:pk>/delete/', views.HelpTextHardDeleteView.as_view(), name="delete_help_text"),
    path('settings/cost-categories/', views.CostCategoryFormsetView.as_view(), name="manage_cost_categories"),
    path('settings/cost-category/<int:pk>/delete/', views.CostCategoryHardDeleteView.as_view(), name="delete_cost_category"),
    path('settings/costs/', views.CostFormsetView.as_view(), name="manage_costs"),
    path('settings/cost/<int:pk>/delete/', views.CostHardDeleteView.as_view(), name="delete_cost"),
    path('settings/njc-rates/', views.NJCRatesFormsetView.as_view(), name="manage_njc_rates"),
    # path('settings/njc-rate/<int:pk>/delete/', views.NJCRatesHardDeleteView.as_view(), name="delete_njc_rate"),
    path('settings/trip-categories/', views.TripCategoryFormsetView.as_view(), name="manage_trip_categories"),
    # path('settings/trip-category/<int:pk>/delete/', views.TripCategoryHardDeleteView.as_view(), name="delete_trip_category"),
    path('settings/trip-subcategories/', views.TripSubcategoryFormsetView.as_view(), name="manage_trip_subcategories"),
    path('settings/trip-subcategory/<int:pk>/delete/', views.TripSubcategoryHardDeleteView.as_view(), name="delete_trip_subcategory"),
    # path('settings/trip-reasons/', views.ReasonFormsetView.as_view(), name="manage_reasons"),
    # path('settings/trip-reasons/<int:pk>/delete/', views.ReasonHardDeleteView.as_view(), name="delete_reason"),

    path('settings/process-steps/', views.ProcessStepFormsetView.as_view(), name="manage_process_steps"),
    path('settings/process-step/<int:pk>/delete/', views.ProcessStepHardDeleteView.as_view(), name="delete_process_step"),

    # default reviewer settings
    path('default-reviewers/', views.DefaultReviewerListView.as_view(), name="default_reviewer_list"),
    path('default-reviewer/new/', views.DefaultReviewerCreateView.as_view(), name="default_reviewer_new"),
    path('default-reviewer/<int:pk>/edit/', views.DefaultReviewerUpdateView.as_view(), name="default_reviewer_edit"),
    path('default-reviewer/<int:pk>/delete/', views.DefaultReviewerDeleteView.as_view(), name="default_reviewer_delete"),

    # TRIP REQUEST COST #
    #####################
    path('trip-request/<int:trip_request>/cost/new/', views.TRCostCreateView.as_view(), name="tr_cost_new"),
    path('trip-request-cost/<int:pk>/edit/', views.TRCostUpdateView.as_view(), name="tr_cost_edit"),
    path('trip-request-cost/<int:pk>/delete/', views.tr_cost_delete, name="tr_cost_delete"),

    path('trip-request/<int:trip_request>/clear-empty-costs/', views.tr_cost_clear, name="tr_cost_clear"),
    path('trip-request/<int:trip_request>/populate-all-costs/', views.tr_cost_populate, name="tr_cost_populate"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/export-cfts-list/year/<str:fy>/region/<str:region>/trip/<str:trip>/traveller/'
         '<str:user>/from_date/<str:from_date>/to_date/<str:to_date>/', views.export_cfts_list, name="export_cfts_list"),
    path('reports/cfts/request/<int:trip_request>/', views.export_request_cfts, name="export_cfts_request"),
    path('reports/cfts/trip/<int:trip>/', views.export_request_cfts, name="export_cfts_trip"),
    # path('event/<int:fy>/<str:email>/print/', views.TravelPlanPDF.as_view(), name="travel_plan"),

    path('reports/trip-list/fiscal-year/<str:fy>/region/<str:region>/adm/<str:adm>/from_date/<str:from_date>/to_date/<str:to_date>/',
         views.export_trip_list, name="export_trip_list"),

    # Download a file
    path('download/file/<int:file>/', views.get_file, name="get_file"),

]
