from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'ios2'
urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.IndexTemplateView.as_view(), name="index"),

    # Instruments #
    ############
    # path('my-list/', views.MyProjectListView.as_view(), name="my_project_list"),
    # path('my-section/', views.MySectionListView.as_view(), name="my_section_list"),
    path('ios2/', views.InstrumentListView.as_view(), name="instrument_list"),
    path('ios2/new/', views.InstrumentCreateView.as_view(), name="instrument_new"),
    path('ios2/<int:pk>/view', views.InstrumentDetailView.as_view(), name="instrument_detail"),
    path('ios2/<int:pk>/submit', views.InstrumentSubmitUpdateView.as_view(), name="instrument_submit"),
    path('ios2/<int:pk>/print', views.InstrumentPrintDetailView.as_view(), name="instrument_print"),
    path('ios2/<int:pk>/delete', views.InstrumentDeleteView.as_view(), name="instrument_delete"),
    path('ios2/<int:pk>/edit', views.InstrumentUpdateView.as_view(), name="instrument_edit"),

    # Moorings
    path('ios2/mooring/', views.MooringListView.as_view(), name="mooring_list"),
    path('ios2/mooring/new/', views.MooringCreateView.as_view(), name="mooring_new"),
    path('ios2/mooring/<int:pk>/view', views.MooringDetailView.as_view(), name="mooring_detail"),

    path('ios2/mooring/<int:pk>/submit', views.MooringSubmitUpdateView.as_view(), name="mooring_submit"),
    path('ios2/mooring/<int:pk>/print', views.MooringPrintDetailView.as_view(), name="mooring_print"),
    path('ios2/mooring/<int:pk>/delete', views.MooringDeleteView.as_view(), name="mooring_delete"),
    path('ios2/mooring/<int:pk>/edit', views.MooringUpdateView.as_view(), name="mooring_edit"),


    # InstrumentDeployments #
    ############
    # path('ios2/<int:instrument>/instrudeployment/new/', views.InstrumentDeploymentCreateView.as_view(),
    #      name="instrudeploy_new"),
    # path('instrudeployment/<int:pk>/populate-all/', views.deployment_populate, name="deployment_populate"),
    # path('instrudeployment/<int:pk>/edit/', views.DeploymentUpdateView.as_view(), name="deployment_edit"),
    # path('instrudeployment/<int:pk>/delete/', views.deployment_delete, name="deployment_delete"),
    # path('ios2/<int:instrument>/clear-empty/', views.deployment_clear, name="deployment_clear"),

    # path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name="staff_edit"),

    # Add instruments to moorings #
    # ############
    path('ios2/mooring/<int:pk>/addinstrument', views.InstrumentMooringCreateView.as_view(), name="add_instrument"),
    path('ios2/<int:pk>/adddeployment', views.MooringInstrumentCreateView.as_view(), name="add_deployment"),

    path('deploymentinstrument/<int:pk>/edit/', views.MooringInstrumentUpdateView.as_view(),
         name="deploymentinstrument_edit"),

    # path('ios2/<int:instrument>/deployment/new/', views.AddDeploymentCreateView.as_view(), name="deploy_new"),
    # path('ios2/deployment/new/', views.DeploymentCreateView.as_view(), name="deploy_new"),
    # path('deployment/<int:pk>/populate-all/', views.deployment_populate, name="deployment_populate"),
    # path('deployment/<int:pk>/edit/', views.DeploymentUpdateView.as_view(), name="deployment_edit"),
    # path('deployment/<int:pk>/delete/', views.deployment_delete, name="deployment_delete"),
    # path('ios2/<int:instrument>/clear-empty/', views.deployment_clear, name="deployment_clear"),
    # path('deployment/<int:pk>/view', views.MooringDetailView.as_view(), name="deployment_detail"),

    path('instrument/<int:pk>/delete/', views.mooringtoinstrument_delete,
         name="mooringtoinstrument_delete"),

    path('deployment/<int:pk>/delete/', views.instrumentonmooring_delete,
         name="instrumentonmooring_delete"),

    # path('instrudeployment/<int:pk>/delete/', views.InstrumentDeploymentDeleteView.as_view(),
    #      name="instrumentondeployment_delete"),

    path('instrudeployment/<int:pk>/edit/', views.InstrumentMooringUpdateView.as_view(),
         name="instrumentmooring_edit"),

    # Service History #
    ############
    path('instrument/<int:instrument>/service/new/', views.ServiceCreateView.as_view(), name="service_new"),
    path('service/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name="service_edit"),
    path('service/<int:pk>/delete/', views.service_delete, name="service_delete"),



]
