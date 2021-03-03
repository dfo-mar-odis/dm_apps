from django.urls import path

from . import views

app_name = 'shared_models'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('close_no_refresh/', views.CloserNoRefreshTemplateView.as_view(), name="close_me_no_refresh"),

    # DFO ORGANIZATION #
    path('dfo-org/', views.IndexTemplateView.as_view(), name="index"),

    # SECTION #
    ###########
    path('sections/', views.SectionListView.as_view(), name="section_list"),  # TESTED
    path('section/<int:pk>/update/', views.SectionUpdateView.as_view(), name="section_edit"),  # TESTED
    path('section/<int:pk>/delete/', views.SectionDeleteView.as_view(), name="section_delete"),  # TESTED
    path('section/new/', views.SectionCreateView.as_view(), name="section_new"),  # TESTED

    # DIVISION #
    ############
    path('divisions/', views.DivisionListView.as_view(), name="division_list"),  # TESTED
    path('division/<int:pk>/update/', views.DivisionUpdateView.as_view(), name="division_edit"),  # TESTED
    path('division/<int:pk>/delete/', views.DivisionDeleteView.as_view(), name="division_delete"),  # TESTED
    path('division/new/', views.DivisionCreateView.as_view(), name="division_new"),  # TESTED

    # BRANCH #
    ############
    path('branches/', views.BranchListView.as_view(), name="branch_list"),  # TESTED
    path('branch/<int:pk>/update/', views.BranchUpdateView.as_view(), name="branch_edit"),  # TESTED
    path('branch/<int:pk>/delete/', views.BranchDeleteView.as_view(), name="branch_delete"),  # TESTED
    path('branch/new/', views.BranchCreateView.as_view(), name="branch_new"),  # TESTED

    # REGION #
    ############
    path('regions/', views.RegionListView.as_view(), name="region_list"),  # TESTED
    path('region/<int:pk>/update/', views.RegionUpdateView.as_view(), name="region_edit"),  # TESTED
    path('region/<int:pk>/delete/', views.RegionDeleteView.as_view(), name="region_delete"),  # TESTED
    path('region/new/', views.RegionCreateView.as_view(), name="region_new"),  # TESTED

    # ORGANIZATION #
    ################
    path('orgs/', views.OrganizationListView.as_view(), name="org_list"),  # TESTED
    path('orgs/<int:pk>/update/', views.OrganizationUpdateView.as_view(), name="org_edit"),  # TESTED
    path('orgs/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name="org_delete"),  # TESTED
    path('orgs/new/', views.OrganizationCreateView.as_view(), name="org_new"),  # TESTED

    # PROJECT CODES #
    ################
    path('project-codes/', views.ProjectCodeListView.as_view(), name="project_list"),
    path('project-codes/new/', views.ProjectCodeCreateView.as_view(), name="project_new"),
    path('project-codes/<int:pk>/edit/', views.ProjectCodeUpdateView.as_view(), name="project_edit"),
    path('project-codes/<int:pk>/delete/', views.ProjectCodeDeleteView.as_view(), name="project_delete"),

    # RESPONSIBILITY CENTER #
    ################
    path('responsibility-centers/', views.ResponsibilityCenterListView.as_view(), name="rc_list"),
    path('responsibility-centers/new/', views.ResponsibilityCenterCreateView.as_view(), name="rc_new"),
    path('responsibility-centers/<int:pk>/edit/', views.ResponsibilityCenterUpdateView.as_view(), name="rc_edit"),
    path('responsibility-centers/<int:pk>/delete/', views.ResponsibilityCenterDeleteView.as_view(), name="rc_delete"),

    # USER # (NOT TESTED)
    ########
    path('user/new/', views.UserCreateView.as_view(), name="user_new"),  # TESTED

    # SCRIPT #
    ##########
    path('scripts/', views.ScriptListView.as_view(), name="script_list"),  # TESTED
    path('script/<int:pk>/edit/', views.ScriptUpdateView.as_view(), name="script_edit"),  # TESTED
    path('script/<int:pk>/delete/', views.ScriptDeleteView.as_view(), name="script_delete"),  # TESTED
    path('script/new/', views.ScriptCreateView.as_view(), name="script_new"),  # TESTED
    path('script/<int:pk>/run/', views.run_script, name="run_script"),  # TESTED

    # REPORTS
    #########

    path('dfo-org/export-report/', views.export_org_report, name="export_org_report"),  # TESTED
]
