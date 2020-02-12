
from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),


#     # Inventory #
#     ###########
    path('species_list/', views.SpeciesListView.as_view(), name="species_list"),
    path('item_list/', views.ItemsListView.as_view(), name="item_list"),
    path('item_detail/<int:pk>/view/', views.ItemsDetailView.as_view(), name="item_detail")
#     # path('species/new/', views.SpeciesCreateView.as_view(), name="item_new"),
#     # path('species/<int:pk>/edit/', views.SpeciesUpdateView.as_view(), name="item_edit"),
#     # path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name="item_delete"),


]

app_name = 'necropsy'
