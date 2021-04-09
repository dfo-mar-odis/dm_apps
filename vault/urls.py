from . import views

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'vault'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.index, name="index"),

    #     # DASHBOARD 1 #
    #     ###########

    # path('dashboard/', views.dashboard_with_pivot, name="dashboard_with_pivot"),
    # path('data/', views.pivot_data, name="pivot_data"),

    # SETTINGS #

    path('admin_tools', views.admin_tools, name="admin_tools"),

    # FORMSETS #

    path('settings/instrument_type/', views.InstrumentTypeFormsetView.as_view(), name="manage_instrument_type"),
    path('settings/instrument_type/<int:pk>/delete/', views.InstrumentTypeHardDeleteView.as_view(),
         name="delete_instrument_type"),
    path('settings/instrument/', views.InstrumentFormsetView.as_view(), name="manage_instrument"),
    path('settings/instrument/<int:pk>/delete/', views.InstrumentHardDeleteView.as_view(),
         name="delete_instrument"),
    path('settings/organisation/', views.OrganisationFormsetView.as_view(), name="manage_organisation"),
    path('settings/organisation/<int:pk>/delete/', views.OrganisationHardDeleteView.as_view(),
         name="delete_organisation"),
    # path('settings/platform_type/', views.ObservationPlatformTypeFormsetView.as_view(), name="manage_platform_type"),
    # path('settings/platform_type/<int:pk>/delete/', views.ObservationPlatformTypeHardDeleteView.as_view(),
    #      name="delete_platform_type"),
    path('settings/platform/', views.ObservationPlatformFormsetView.as_view(), name="manage_platform"),
    path('settings/platform/<int:pk>/delete/', views.ObservationPlatformHardDeleteView.as_view(),
         name="delete_platform"),
    path('settings/role/', views.RoleFormsetView.as_view(), name="manage_role"),
    path('settings/role/<int:pk>/delete/', views.RoleHardDeleteView.as_view(), name="delete_role"),
    path('settings/person/', views.PersonFormsetView.as_view(), name="manage_person"),
    path('settings/person/<int:pk>/delete/', views.PersonHardDeleteView.as_view(), name="delete_person"),


    # ADMIN USERS #
    path('settings/users/', views.UserListView.as_view(), name='user_list'),
    path('settings/users/vault/<int:vault>/', views.UserListView.as_view(), name='user_list'),
    path('settings/user/<int:pk>/toggle/<str:type>/', views.toggle_user, name='toggle_user'),

    # SPECIES #

    path('species-list/', views.SpeciesListView.as_view(), name="species_list"),
    path('species/new/', views.SpeciesCreateView.as_view(), name="species_new"),
    path('species/<int:pk>/view/', views.SpeciesDetailView.as_view(), name="species_detail"),
    path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="species_edit"),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="species_delete"),

    # OUTING #

    path('outing-list/', views.OutingListView.as_view(), name="outing_list"),
    path('outing/new/', views.OutingCreateView.as_view(), name="outing_new"),
    path('outing/<int:pk>/view/', views.OutingDetailView.as_view(), name="outing_detail"),
    path('outing/<int:pk>/edit/', views.OutingUpdateView.as_view(), name="outing_edit"),
    path('outing/<int:pk>/delete/', views.OutingDeleteView.as_view(), name="outing_delete"),

    # OBSERVATION #

    path('observation-list/', views.ObservationListView.as_view(), name="observation_list"),
    path('observation/new/', views.ObservationCreateView.as_view(), name="observation_new"),
    path('observation/<int:pk>/view/', views.ObservationDetailView.as_view(), name="observation_detail"),
    path('observation/<int:pk>/edit/', views.ObservationUpdateView.as_view(), name="observation_edit"),
    path('observation/<int:pk>/delete/', views.ObservationDeleteView.as_view(), name="observation_delete"),
]
