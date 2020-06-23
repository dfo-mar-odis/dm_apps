from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),
    path('route/<int:pk>/view/', views.RouteDetailView.as_view(), name="route_detail"),

    # sign me up / remove me
    path('route/<int:route>/sign-up-or-remove-user/', views.sign_up_or_remove_user_from_route, name="sign_up_or_remove_user_from_route"),

    # outing form
    path('outing/<int:pk>/edit/', views.OutingUpdateView.as_view(), name="outing_edit"),

]
app_name = 'spring_cleanup'
