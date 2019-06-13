from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'staff'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),
    path('planning', views.CreatePlan.as_view(), name="create_plan"),
    path('planning/<int:pk>', views.UpdatePlan.as_view(), name="update_plan"),
]
