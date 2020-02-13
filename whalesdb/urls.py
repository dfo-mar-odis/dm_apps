from django.urls import path
from . import views

app_name = 'whalesdb'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),

    path('create/stn', views.CreateStn.as_view(), name="create_stn"),
    path('details/<int:pk>/stn', views.DetailsStn.as_view(), name="details_stn"),
    path('list/stn/', views.ListStn.as_view(), name="list_stn"),

    path('create/prj', views.CreatePrj.as_view(), name="create_prj"),
    path('details/<int:pk>/prj', views.DetailsPrj.as_view(), name="details_prj"),
    path('list/prj/', views.ListPrj.as_view(), name="list_prj"),

    path('create/mor', views.CreateMor.as_view(), name="create_mor"),
    path('details/<int:pk>/mor', views.DetailsMor.as_view(), name="details_mor"),
    path('list/mor/', views.ListMor.as_view(), name="list_mor"),
]
