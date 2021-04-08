from django.urls import path

from . import views

urlpatterns = [
    path("ihub/entries/csv/", views.EntryCSVAPIView.as_view(), name="ihub-entry-csv-list"),
]
