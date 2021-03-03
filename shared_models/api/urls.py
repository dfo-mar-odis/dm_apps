from django.urls import path

from . import views

urlpatterns = [
    path("current-user/", views.CurrentUserAPIView.as_view(), name="current-user"),  # tested

    # this should probably be moved to the shared models API, when created
    path("users/", views.UserListAPIView.as_view(), name="user-list"),


    # lookups
    path("fiscal-years/", views.FiscalYearListAPIView.as_view(), name="fiscal-year-list"),
    path("regions/", views.RegionListAPIView.as_view(), name="region-list"),
    path("divisions/", views.DivisionListAPIView.as_view(), name="division-list"),
    path("sections/", views.SectionListAPIView.as_view(), name="section-list"),


]
