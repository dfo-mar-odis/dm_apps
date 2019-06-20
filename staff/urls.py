from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'staff'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),

    path('', views.IndexTemplateView.as_view(), name="index"),
    path('planning', views.CreatePlan.as_view(), name="create_plan"),
    path('planning/<int:pk>', views.UpdatePlan.as_view(), name="update_plan"),
    path('planning/detail/<int:pk>', views.DetailPlan.as_view(), name="detail_plan"),
    path('planning/delfunding/<int:pk>', views.fc_delete, name="delete_funding"),
    path('planning/newfunding/<int:pk>', views.CreateFunding.as_view(), name="new_funding"),
    path('planning/updatefunding/<int:pk>', views.UpdateFunding.as_view(), name="update_funding"),
]
