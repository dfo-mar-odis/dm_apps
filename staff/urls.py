from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'staff'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

]
