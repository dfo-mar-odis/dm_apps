from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shared_models'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('close_no_refresh/', views.CloserNoRefreshTemplateView.as_view(), name="close_me_no_refresh"),

    # DFO ORGANIZATION #
    path('dfo-org/', views.IndexTemplateView.as_view(), name="index"),

    # SECTION #
    ###########
    path('sections/', views.SectionListView.as_view(), name="section_list"),
    path('section/<int:pk>/update/', views.SectionUpdateView.as_view(), name="section_edit"),
    path('section/<int:pk>/delete/', views.SectionDeleteView.as_view(), name="section_delete"),
    path('section/new/', views.SectionCreateView.as_view(), name="section_new"),

    # DIVISION #
    ############
    path('divisions/', views.DivisionListView.as_view(), name="division_list"),
    path('division/<int:pk>/update/', views.DivisionUpdateView.as_view(), name="division_edit"),
    path('division/<int:pk>/delete/', views.DivisionDeleteView.as_view(), name="division_delete"),
    path('division/new/', views.DivisionCreateView.as_view(), name="division_new"),


    # BRANCH #
    ############
    path('branches/', views.BranchListView.as_view(), name="branch_list"),
    path('branch/<int:pk>/update/', views.BranchUpdateView.as_view(), name="branch_edit"),
    path('branch/<int:pk>/delete/', views.BranchDeleteView.as_view(), name="branch_delete"),
    path('branch/new/', views.BranchCreateView.as_view(), name="branch_new"),

    # REGION #
    ############
    path('regions/', views.RegionListView.as_view(), name="region_list"),
    path('region/<int:pk>/update/', views.RegionUpdateView.as_view(), name="region_edit"),
    path('region/<int:pk>/delete/', views.RegionDeleteView.as_view(), name="region_delete"),
    path('region/new/', views.RegionCreateView.as_view(), name="region_new"),

]
