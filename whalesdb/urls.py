from django.urls import path
from . import views

app_name = 'whalesdb'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('close', views.CloserTemplateView.as_view(), name="close_me"),

    path('create/dep/', views.CreateDep.as_view(), name="create_dep"),
    path('update/dep/<int:pk>/', views.UpdateDep.as_view(), name="update_dep"),
    path('details/dep/<int:pk>/', views.DetailsDep.as_view(), name="details_dep"),
    path('list/dep/', views.ListDep.as_view(), name="list_dep"),

    path('create/mor/', views.CreateMor.as_view(), name="create_mor"),
    path('update/mor/<int:pk>/', views.UpdateMor.as_view(), name="update_mor"),
    path('details/mor/<int:pk>/', views.DetailsMor.as_view(), name="details_mor"),
    path('list/mor/', views.ListMor.as_view(), name="list_mor"),

    path('create/prj/', views.CreatePrj.as_view(), name="create_prj"),
    path('update/prj/<int:pk>/', views.UpdatePrj.as_view(), name="update_prj"),
    path('details/prj/<int:pk>/', views.DetailsPrj.as_view(), name="details_prj"),
    path('list/prj/', views.ListPrj.as_view(), name="list_prj"),

    path('create/ste/<int:dep_id>/<int:set_id>/', views.CreateSte.as_view(), name="create_ste"),
    path('create/ste/<int:dep_id>/', views.CreateSte.as_view(), name="create_ste"),

    path('create/stn/', views.CreateStn.as_view(), name="create_stn"),
    path('update/stn/<int:pk>/', views.UpdateStn.as_view(), name="update_stn"),
    path('details/stn/<int:pk>/', views.DetailsStn.as_view(), name="details_stn"),
    path('list/stn/', views.ListStn.as_view(), name="list_stn"),
]
