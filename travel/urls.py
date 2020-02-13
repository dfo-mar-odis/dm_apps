from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

    # TRIP REQUEST #
    ################
    path('requests/', views.TripRequestListView.as_view(), name="request_list"),
    path('request/new/', views.TripRequestCreateView.as_view(), name="request_new"),
    path('request/<int:pk>/view/', views.TripRequestDetailView.as_view(), name="request_detail"),
    path('request/<int:pk>/print/', views.TravelPlanPDF.as_view(), name="request_print"),
    path('request/<int:pk>/edit/', views.TripRequestUpdateView.as_view(), name="request_edit"),
    path('request/<int:pk>/edit/<str:pop>/', views.TripRequestUpdateView.as_view(), name="request_edit"),
    path('request/<int:pk>/delete/', views.TripRequestDeleteView.as_view(), name="request_delete"),
    path('request/<int:pk>/delete/pop/<str:pop>/', views.TripRequestDeleteView.as_view(), name="request_delete"),
    path('request/<int:pk>/duplicate/', views.TripRequestCloneUpdateView.as_view(), name="duplicate_event"),
    path('request/<int:parent_request>/new-child-request/', views.TripRequestCreateView.as_view(), name="request_new"),
    path('request/<int:pk>/clone-child/pop/<str:pop>', views.ChildTripRequestCloneUpdateView.as_view(), name="child_duplicate_event"),
    path('request/<int:pk>/submit/', views.TripRequestSubmitUpdateView.as_view(), name="request_submit"),
    path('request/<int:pk>/cancel/', views.TripRequestCancelUpdateView.as_view(), name="request_cancel"),
    path('request/<int:pk>/admin-notes/', views.TripRequestAdminNotesUpdateView.as_view(), name="admin_notes_edit"),
    path('request/<int:pk>/re-add-reviewers/', views.reset_reviewers, name="reset_reviewers"),

    # REVIEWER APPROVAL
    path('requests/review/', views.TripRequestReviewListView.as_view(), name="request_review_list"),
    path('requests/review/<str:which_ones>/', views.TripRequestReviewListView.as_view(), name="request_review_list"),
    path('review/<int:pk>/approve/', views.ReviewerApproveUpdateView.as_view(), name="review_approve"),
    path('review/<int:pk>/skip/', views.SkipReviewerUpdateView.as_view(), name="reviewer_skip"),

    # ADMIN APPROVAL
    path('admin/approval/', views.TripRequestAdminApprovalListView.as_view(), name="admin_approval_list"),
    # path('admin/<int:pk>/approve/', views.TripRequestAdminApproveUpdateView.as_view(), name="admin_approve"),

    # REVIEWERS #
    #############
    path('request/<int:trip_request>/manage-reviewers/', views.manage_reviewers, name="manage_reviewers"),
    path('reviewer/<int:pk>/delete/', views.delete_reviewer, name="delete_reviewer"),

    # TRIP #
    ########
    path('trips/', views.TripListView.as_view(), name="trip_list"),
    path('trip/new/', views.TripCreateView.as_view(), name="trip_new"),
    path('trip/new/pop/<int:pop>/', views.TripCreateView.as_view(), name="trip_new"),
    path('trip/<int:pk>/view/', views.TripDetailView.as_view(), name="trip_detail"),
    path('trip/<int:pk>/edit/', views.TripUpdateView.as_view(), name="trip_edit"),
    path('trip/<int:pk>/delete/', views.TripDeleteView.as_view(), name="trip_delete"),
    # admin
    path('admin/trip-verification-list/', views.AdminTripVerificationListView.as_view(), name="admin_trip_verification_list"),
    path('trip/<int:pk>/verify/', views.TripVerifyUpdateView.as_view(), name="trip_verify"),

    # FILES #
    #########
    path('request/<int:trip_request>/file/new/', views.FileCreateView.as_view(), name='file_new'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/export-cfts-list/year/<int:fy>/user/<int:user>/', views.export_cfts_list, name="export_cfts_list"),
    path('reports/cfts/request/<int:trip_request>/', views.export_request_cfts, name="export_cfts_request"),
    path('reports/cfts/trip/<int:trip>/', views.export_request_cfts, name="export_cfts_trip"),
    # path('event/<int:fy>/<str:email>/print/', views.TravelPlanPDF.as_view(), name="travel_plan"),

    # SETTINGS #
    ############
    path('settings/statuses/', views.manage_statuses, name="manage_statuses"),
    path('settings/status/<int:pk>/delete/', views.delete_status, name="delete_status"),
    path('settings/help-text/', views.manage_help_text, name="manage_help_text"),
    path('settings/help-text/<int:pk>/delete/', views.delete_help_text, name="delete_help_text"),
    path('settings/cost-categories/', views.manage_cost_categories, name="manage_cost_categories"),
    path('settings/cost-category/<int:pk>/delete/', views.delete_cost_category, name="delete_cost_category"),
    path('settings/costs/', views.manage_costs, name="manage_costs"),
    path('settings/cost/<int:pk>/delete/', views.delete_cost, name="delete_cost"),
    path('settings/njc-rates/', views.manage_njc_rates, name="manage_njc_rates"),
    path('settings/njc-rate/<int:pk>/delete/', views.delete_njc_rate, name="delete_njc_rate"),

    # TRIP REQUEST COST #
    #####################
    path('trip-request/<int:trip_request>/cost/new/', views.TRCostCreateView.as_view(), name="tr_cost_new"),
    path('trip-request-cost/<int:pk>/edit/', views.TRCostUpdateView.as_view(), name="tr_cost_edit"),
    path('trip-request-cost/<int:pk>/delete/', views.tr_cost_delete, name="tr_cost_delete"),

    path('trip-request/<int:trip_request>/clear-empty-costs/', views.tr_cost_clear, name="tr_cost_clear"),
    path('trip-request/<int:trip_request>/populate-all-costs/', views.tr_cost_populate, name="tr_cost_populate"),

]
