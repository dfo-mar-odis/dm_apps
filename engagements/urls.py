from django.urls import path
from . import views

app_name = 'engagements'

urlpatterns = [
    path('', views.engagements_home, name='home'),

    # Organizations
    path('organizations/', views.OrganizationListView.as_view(), name='organization_list'),
    path('organizations/add', views.OrganizationCreateView.as_view(), name='organization_create'),
    path('organizations/<slug:slug>', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('organizations/<slug:slug>/edit', views.OrganizationUpdateView.as_view(), name='organization_update'),
    path('organizations/<slug:slug>/delete', views.OrganizationDeleteView.as_view(), name='organization_delete'),
    
    # Individuals
    path('individuals/', views.IndividualListView.as_view(), name='individual_list'),
    path('individuals/add', views.IndividualCreateView.as_view(), name='individual_create'),
    path('individuals/<slug:slug>', views.IndividualDetailView.as_view(), name='individual_detail'),
    path('individuals/<slug:slug>/edit', views.IndividualUpdateView.as_view(), name='individual_update'),
    path('individuals/<slug:slug>/delete', views.IndividualDeleteView.as_view(), name='individual_delete'),

    # Engagement plans
    path('plans/', views.PlanListView.as_view(), name='plan_list'),
    path('plans/add', views.PlanCreateView.as_view(), name='plan_create'),
    path('plans/<slug:slug>', views.PlanDetailView.as_view(), name='plan_detail'),
    path('plans/<slug:slug>/edit', views.PlanUpdateView.as_view(), name='plan_update'),
    path('plans/<slug:slug>/delete', views.PlanDeleteView.as_view(), name='plan_delete'),

    # Interactions
    path('interactions/', views.InteractionListView.as_view(), name='interaction_list'),
    path('interactions/add', views.InteractionCreateView.as_view(), name='interaction_create'),
    path('interactions/<slug:slug>', views.InteractionDetailView.as_view(), name='interaction_detail'),
    path('interactions/<slug:slug>/edit', views.InteractionUpdateView.as_view(), name='interaction_update'),
    path('interactions/<slug:slug>/delete', views.InteractionDeleteView.as_view(), name='interaction_delete'),
]
