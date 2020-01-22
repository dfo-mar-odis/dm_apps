from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'oceanography'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),


    # MISSIONS #
    ############
    path('missions/', views.MissionListView.as_view(), name='mission_list'),
    path('mission/<int:pk>/view/', views.MissionDetailView.as_view(), name='mission_detail'),
    path('mission/<int:pk>/edit/', views.MissionUpdateView.as_view(), name='mission_edit'),
    path('mission/new/', views.MissionCreateView.as_view(), name='mission_new'),
    path('mission/<int:pk>/export-csv/', views.export_mission_csv, name='mission_export_csv'),

    # BOTTLES #
    ###########
    path('missions/<int:mission>/bottles/', views.BottleListView.as_view(), name='bottle_list'),
    path('bottles/<int:pk>/view/', views.BottleDetailView.as_view(), name='bottle_detail'),
    path('bottles/<int:pk>/edit/', views.BottleUpdateView.as_view(), name='bottle_edit'),

    # FILES #
    #########
    path('mission/<int:mission>/file/new/', views.FileCreateView.as_view(), name='file_create'),
    path('file/<int:pk>/view/', views.FileDetailView.as_view(), name='file_detail'),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name='file_edit'),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),

    # SETTINGS #
    ############
    path('settings/help-text/', views.manage_help_text, name="manage_help_text"),
    path('settings/help-text/<int:pk>/delete/', views.delete_help_text, name="delete_help_text"),

]

 # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
