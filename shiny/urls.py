from django.urls import path
from . import views

app_name = 'shiny'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),
    path('app/create/', views.AppCreateView.as_view(), name="create"),
    path('app/<int:pk>/edit/', views.AppUpdateView.as_view(), name="update"),
    path('app/<int:pk>/delete/', views.AppDeleteView.as_view(), name="delete"),

]
