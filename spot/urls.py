from django.urls import path
from . import views

app_name = 'spot'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.IndexTemplateView.as_view(), name="index"),

    # ORGANIZATION #
    ################
    path('orgs/', views.OrganizationListView.as_view(), name="org_list"),
    path('org/new/', views.OrganizationCreateView.as_view(), name="org_new"),
    path('org/<int:pk>/view/', views.OrganizationDetailView.as_view(), name="org_detail"),
    path('org/<int:pk>/edit/', views.OrganizationUpdateView.as_view(), name="org_edit"),
    path('org/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name="org_delete"),

    # ORGANIZATION MEMBER #
    ######################
    path('org/<int:org>/member/new/', views.MemberCreateView.as_view(), name="member_new"),
    path('member/<int:pk>/edit/', views.MemberUpdateView.as_view(), name="member_edit"),
    path('member/<int:pk>/delete/', views.MemberDeleteView.as_view(), name="member_delete"),

    # PERSON #
    ##########
    path('people/', views.PersonListView.as_view(), name="person_list"),
    path('person/new/', views.PersonCreateView.as_view(), name="person_new"),
    path('person/new/popout/', views.PersonCreateViewPopout.as_view(), name="person_new_pop"),
    path('person/<int:pk>/view/', views.PersonDetailView.as_view(), name="person_detail"),
    path('person/<int:pk>/edit/', views.PersonUpdateView.as_view(), name="person_edit"),
    path('person/<int:pk>/edit/popout/', views.PersonUpdateViewPopout.as_view(), name="person_edit_pop"),
    path('person/<int:pk>/delete/', views.PersonDeleteView.as_view(), name="person_delete"),

    # PROJECT #
    ###########
    path('projects/', views.ProjectListView.as_view(), name="project_list"),
    path('project/new/', views.ProjectCreateView.as_view(), name="project_new"),
    path('project/<int:pk>/view/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name="project_edit"),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name="project_delete"),

    # Tracking views
    path('<int:pk>/tracking/<str:step>/', views.TrackingUpdateView.as_view(), name="tracking"),
    path('project/<int:pk>/eoi/', views.EOIUpdateView.as_view(), name="eoi"),
    path('project/<int:pk>/ca-checklist/', views.CAChecklistUpdateView.as_view(), name="ca_checklist"),


    # PROJECT PERSON #
    ##################
    path('project/<int:project>/person/new/', views.ProjectPersonCreateView.as_view(), name="project_person_new"),
    path('project-person/<int:pk>/edit/', views.ProjectPersonUpdateView.as_view(), name="project_person_edit"),
    path('project-person/<int:pk>/delete/', views.ProjectPersonDeleteView.as_view(), name="project_person_delete"),
    path('user-to-person/<int:user>/return-to/<str:view_name>/pk/<int:pk>/', views.user_to_person, name="user_to_person"),

    # PROJECT YEAR #
    ################
    path('project/<int:project>/year/new/', views.ProjectYearCreateView.as_view(), name="year_new"),
    path('project-year/<int:pk>/view/', views.ProjectYearDetailView.as_view(), name="year_detail"),
    path('project-year/<int:pk>/edit/', views.ProjectYearUpdateView.as_view(), name="year_edit"),
    path('project-year/<int:pk>/delete/', views.ProjectYearDeleteView.as_view(), name="year_delete"),

    # Tracking views
    path('project-year/<int:pk>/tracking/<str:step>/', views.TrackingUpdateView.as_view(), name="tracking"),


    # PAYMENT #
    ###########
    path('project-year/<int:project_year>/payment/new/', views.PaymentCreateView.as_view(), name="payment_new"),
    path('payment/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name="payment_edit"),
    path('payment/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name="payment_delete"),

    # FILE #
    ########
    path('project/<int:project>/file/new/', views.FileCreateView.as_view(), name="file_new"),
    path('project/<int:project>/file/new/file-type/<int:type>/', views.FileCreateView.as_view(), name="file_new"),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name="file_edit"),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name="file_delete"),

    # path('file/<int:pk>/delete/', views.file_delete, name="file_delete"),

    #
    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/negotiations/<int:fy>/<str:programs>/', views.NegotiationReport.as_view(), name="report_neg"),
    # path('reports/export-custom-list/<str:provinces>/<str:groupings>/<str:sectors>/<str:regions>/<int:is_indigenous>/<str:species>', views.export_custom_list, name="export_custom_list"),



]
