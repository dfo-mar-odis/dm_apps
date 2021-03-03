from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'trips', views.TripViewSet)
router.register(r'requests', views.RequestViewSet)
router.register(r'travellers', views.TravellerViewSet)
router.register(r'request-reviewers', views.ReviewerViewSet)
router.register(r'trip-reviewers', views.TripReviewerViewSet)
router.register(r'request-files', views.FileViewSet)
router.register(r'costs', views.CostViewSet)

urlpatterns = [
    path("travel/", include(router.urls)),
    path("travel/user/", views.CurrentTravelUserAPIView.as_view(), name="travel-current-user"),
    path("travel/help-text/", views.HelpTextAPIView.as_view(), name="travel-current-user"),
    path("travel/admin-warnings/", views.AdminWarningsAPIView.as_view(), name="travel-current-user"),


    # lookups
    path("travel/fiscal-years/", views.FiscalYearTravelListAPIView.as_view(), name="travel-fiscal-year-list"),
    path("travel/regions/", views.RegionListAPIView.as_view(), name="travel-region-list"),
    path("travel/divisions/", views.DivisionListAPIView.as_view(), name="travel-division-list"),
    path("travel/sections/", views.SectionListAPIView.as_view(), name="travel-section-list"),

    path("travel/meta/models/request/", views.RequestModelMetaAPIView.as_view(), name="reviewer-model-meta"),
    path("travel/meta/models/trip/", views.TripModelMetaAPIView.as_view(), name="reviewer-model-meta"),
    path("travel/meta/models/request-reviewer/", views.ReviewerModelMetaAPIView.as_view(), name="reviewer-model-meta"),
    path("travel/meta/models/trip-reviewer/", views.TripReviewerModelMetaAPIView.as_view(), name="reviewer-model-meta"),
    path("travel/meta/models/traveller/", views.TravellerModelMetaAPIView.as_view(), name="traveller-model-meta"),
    path("travel/meta/models/file/", views.FileModelMetaAPIView.as_view(), name="file-model-meta"),
    path("travel/meta/models/cost/", views.CostModelMetaAPIView.as_view(), name="cost-model-meta"),

]
