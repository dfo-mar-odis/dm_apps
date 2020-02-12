
from . import views

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),

    # path('admin/', admin.site.urls),

#     # SPECIES #
#     ###########
    path('species-list/', views.SpeciesListView.as_view(), name="species_list"),
    path('species/new/', views.SpeciesCreateView.as_view(), name="species_new"),
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),
    path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),

# # INSTRUMENTS #
    path('instrument-list/', views.InstrumentListView.as_view(), name="instrument_list"),
    path('instrument/new/', views.InstrumentCreateView.as_view(), name="instrument_new"),
    path('instrument/<int:pk>/view/', views.InstrumentDetailView.as_view(), name="instrument_detail"),
    path('instrument/<int:pk>/edit/', views.InstrumentUpdateView.as_view(), name="instrument_edit"),
    path('instrument/<int:pk>/delete/', views.InstrumentDeleteView.as_view(), name="instrument_delete"),

]

app_name = 'vault'
