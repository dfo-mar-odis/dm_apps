from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'grainsize'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    
    path('country/', views.CountryListView.as_view(), name='country'),
    path('country/add/', views.CountryCreate.as_view(), name='country_add'),
    path('country/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('country/<slug:slug>/delete', views.CountryDelete.as_view(), name='country_delete'),
    path('country/<slug:slug>/update', views.CountryUpdate.as_view(), name='country_update'),

    path('project/', views.ProjectListView.as_view(), name='project_list'),
    path('project/add/', views.ProjectCreate.as_view(), name='project_add'),
    path('project/<project>/samples', views.ProjectSampleList.as_view(), name='project_samples'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/delete', views.ProjectDelete.as_view(), name='project_delete'),
    path('project/<int:pk>/update', views.ProjectUpdate.as_view(), name='project_update'),

    path('analysis/', views.AnalysisListView.as_view(), name='analysis'),
    path('analysis/add/', views.AnalysisCreate.as_view(), name='analysis_add'),
    path('analysis/<int:pk>/', views.AnalysisDetailView.as_view(), name='analysis_detail'),
    path('analysis/<int:pk>/delete', views.AnalysisDelete.as_view(), name='analysis_delete'),
    path('analysis/<int:pk>/update', views.AnalysisUpdate.as_view(), name='analysis_update'),

    path('collection/', views.CollectionListView.as_view(), name='collection'),
    path('collection/add/', views.CollectionCreate.as_view(), name='collection_add'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collection/<int:pk>/delete', views.CollectionDelete.as_view(), name='collection_delete'),
    path('collection/<int:pk>/update', views.CollectionUpdate.as_view(), name='collection_update'),

    path('preservation/', views.PreservationListView.as_view(), name='preservation'),
    path('preservation/add/', views.PreservationCreate.as_view(), name='preservation_add'),
    path('preservation/<int:pk>/', views.PreservationDetailView.as_view(), name='preservation_detail'),
    path('preservation/<int:pk>/delete', views.PreservationDelete.as_view(), name='preservation_delete'),
    path('preservation/<int:pk>/update', views.PreservationUpdate.as_view(), name='preservation_update'),

    path('sampletype/', views.SampleTypeListView.as_view(), name='sampletype'),
    path('sampletype/add/', views.SampleTypeCreate.as_view(), name='sampletype_add'),
    path('sampletype/<int:pk>/', views.SampleTypeDetailView.as_view(), name='sampletype_detail'),
    path('sampletype/<int:pk>/delete', views.SampleTypeDelete.as_view(), name='sampletype_delete'),
    path('sampletype/<int:pk>/update', views.SampleTypeUpdate.as_view(), name='sampletype_update'),

    path('storagetype/', views.StorageTypeListView.as_view(), name='storagetype'),
    path('storagetype/add/', views.StorageTypeCreate.as_view(), name='storagetype_add'),
    path('storagetype/<int:pk>/', views.StorageTypeDetailView.as_view(), name='storagetype_detail'),
    path('storagetype/<int:pk>/delete', views.StorageTypeDelete.as_view(), name='storagetype_delete'),
    path('storagetype/<int:pk>/update', views.StorageTypeUpdate.as_view(), name='storagetype_update'),

    path('sample/', views.SampleListView.as_view(), name='sample'),
    path('sample/add/', views.SampleCreate.as_view(), name='sample_add'),
    path('sample/<sample>/data', views.SampleDataList.as_view(), name='sample_data'),
    path('sample/<int:pk>/', views.SampleDetailView.as_view(), name='sample_detail'),
    path('sample/<int:pk>/delete', views.SampleDelete.as_view(), name='sample_delete'),
    path('sample/<int:pk>/update', views.SampleUpdate.as_view(), name='sample_update'),

    path('data/', views.DataListView.as_view(), name='data'),
    path('data/add/', views.DataCreate.as_view(), name='data_add'),
    path('data/<int:pk>/', views.DataDetailView.as_view(), name='data_detail'),
    path('data/<int:pk>/delete', views.DataDelete.as_view(), name='data_delete'),
    path('data/<int:pk>/update', views.DataUpdate.as_view(), name='data_update'),
]
