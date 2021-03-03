from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("pageviews/", views.PageViewsAPIView.as_view(), name="page-views"),
]
