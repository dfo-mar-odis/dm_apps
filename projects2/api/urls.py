from django.urls import path

from . import views

urlpatterns = [
    path("project-planning/user/", views.CurrentUserAPIView.as_view(), name="projects2-current-user"),  # tested
    path("project-planning/fte-breakdown/", views.FTEBreakdownAPIView.as_view(), name="projects2-fte-breakdown"),  # tested

    # Project
    path("project-planning/projects/<int:pk>/", views.ProjectRetrieveAPIView.as_view(), name="projects2-project-detail"),  # tested
    path("project-planning/projects/<int:pk>/reference/<str:action>/", views.AddProjectReferenceAPIView.as_view(), name="projects2-project-reference"),  # tested
    path("project-planning/projects/", views.ProjectListAPIView.as_view(), name="projects2-project-list"),  # tested

    # Project year
    path("project-planning/project-years/", views.ProjectYearListAPIView.as_view(), name="projects2-year-list"),  # tested
    path("project-planning/project-years/<int:pk>/", views.ProjectYearRetrieveAPIView.as_view(), name="projects2-year-detail"),  # tested
    path("project-planning/project-years/<int:project_year>/submit/", views.ProjectYearSubmitAPIView.as_view(), name="projects2-year-submit"),  # tested
    path("project-planning/project-years/<int:project_year>/unsubmit/", views.ProjectYearUnsubmitAPIView.as_view(), name="projects2-year-unsubmit"),  # tested

    # Staff
    path("project-planning/project-years/<int:project_year>/staff/", views.StaffListCreateAPIView.as_view(), name="projects2-staff-list"),  # tested
    path("project-planning/staff/<int:pk>/", views.StaffRetrieveUpdateDestroyAPIView.as_view(), name="projects2-staff-detail"),
    path("project-planning/get-dates/", views.GetDatesAPIView.as_view(), name="projects2-get-dates"),

    # O&M
    path("project-planning/project-years/<int:project_year>/om-costs/", views.OMCostListCreateAPIView.as_view(), name="projects2-om-list"),  # tested
    path("project-planning/om-costs/<int:pk>/", views.OMCostRetrieveUpdateDestroyAPIView.as_view(), name="projects2-om-detail"),
    path("project-planning/project-years/<int:project_year>/add-all-costs/", views.AddAllCostsAPIView.as_view(), name="projects2-add-all-costs"),
    path("project-planning/project-years/<int:project_year>/remove-empty-costs/", views.RemoveEmptyCostsAPIView.as_view(), name="projects2-remove-empty-costs"),

    # Capital
    path("project-planning/project-years/<int:project_year>/capital-costs/", views.CapitalCostListCreateAPIView.as_view(), name="projects2-capital-list"),  # tested
    path("project-planning/capital-costs/<int:pk>/", views.CapitalCostRetrieveUpdateDestroyAPIView.as_view(), name="projects2-capital-detail"),

    # GC
    # path("project-planning/project-years/<int:project_year>/gc-costs/", views.GCCostListCreateAPIView.as_view(), name="gc-list"),  # tested
    # path("project-planning/gc-costs/<int:pk>/", views.GCCostRetrieveUpdateDestroyAPIView.as_view(), name="gc-detail"),

    # activities
    path("project-planning/project-years/<int:project_year>/activities/", views.ActivityListCreateAPIView.as_view(), name="projects2-activity-list"),  # tested
    path("project-planning/activities/<int:pk>/", views.ActivityRetrieveUpdateDestroyAPIView.as_view(), name="projects2-activity-detail"),

    # collaborations
    path("project-planning/project-years/<int:project_year>/collaborations/", views.CollaborationListCreateAPIView.as_view(), name="projects2-collaboration-list"),  # tested
    path("project-planning/collaborations/<int:pk>/", views.CollaborationRetrieveUpdateDestroyAPIView.as_view(), name="projects2-collaboration-detail"),

    # files
    path("project-planning/project-years/<int:project_year>/files/", views.FileListCreateAPIView.as_view(), name="projects2-file-list"),  # tested
    path("project-planning/files/<int:pk>/", views.FileRetrieveUpdateDestroyAPIView.as_view(), name="projects2-file-detail"),

    # status reports
    path("project-planning/project-years/<int:project_year>/status-reports/", views.StatusReportListCreateAPIView.as_view(), name="projects2-status-report-list"),
    # tested
    path("project-planning/status-reports/<int:pk>/", views.StatusReportRetrieveUpdateDestroyAPIView.as_view(), name="projects2-status-report-detail"),
    path("project-planning/status-reports/<int:status_report>/updates/", views.ActivityUpdateListAPIView.as_view(),
         name="activity-update-list"),
    path("project-planning/activity-updates/<int:pk>/", views.ActivityUpdateRetrieveUpdateAPIView.as_view(),
         name="activity-update-detail"),

    # financials
    path("project-planning/project-years/<int:project_year>/financials/", views.FinancialsAPIView.as_view(), name="projects2-financials"),
    path("project-planning/projects/<int:project>/financials/", views.FinancialsAPIView.as_view(), name="projects2-financials"),
    path("project-planning/financials/", views.FinancialsAPIView.as_view(), name="projects2-financials"),

    # lookups
    path("project-planning/fiscal-years/", views.FiscalYearListAPIView.as_view(), name="projects2-fiscal-year-list"),
    path("project-planning/tags/", views.TagListAPIView.as_view(), name="projects2-tag-list"),
    path("project-planning/themes/", views.ThemeListAPIView.as_view(), name="projects2-theme-list"),
    path("project-planning/functional-groups/", views.FunctionalGroupListAPIView.as_view(), name="projects2-group-list"),
    path("project-planning/funding-sources/", views.FundingSourceListAPIView.as_view(), name="projects2-funding-source-list"),
    path("project-planning/regions/", views.RegionListAPIView.as_view(), name="projects2-region-list"),
    path("project-planning/divisions/", views.DivisionListAPIView.as_view(), name="projects2-division-list"),
    path("project-planning/sections/", views.SectionListAPIView.as_view(), name="projects2-section-list"),

    # Reviews
    path("project-planning/project-years/<int:project_year>/reviews/", views.ReviewListCreateAPIView.as_view(), name="projects2-review-list"),
    path("project-planning/reviews/<int:pk>/", views.ReviewRetrieveUpdateDestroyAPIView.as_view(), name="projects2-review-detail"),

    # citations
    path("project-planning/citations/", views.CitationListCreateAPIView.as_view(), name="projects2-citation-list"),
    path("project-planning/citations/<int:pk>/", views.CitationRetrieveUpdateDestroyAPIView.as_view(), name="projects2-citation-detail"),

    # publications
    path("project-planning/publications/", views.PublicationListAPIView.as_view(), name="projects2-publication-list"),
    # path("project-planning/publication/<int:pk>/", views.PublicationRetrieveUpdateDestroyAPIView.as_view(), name="publication-detail"),

    # model lookups
    path("project-planning/meta/models/activity/", views.ActivityModelMetaAPIView.as_view(), name="projects-activity-model-meta"),
    path("project-planning/meta/models/om-cost/", views.OMCostModelMetaAPIView.as_view(), name="projects-omcost-model-meta"),

]
