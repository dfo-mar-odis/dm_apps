from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    # Tickets #
    ###########
    path('', views.index_router, name="router"),
    path('all-tickets/', views.TicketListView.as_view(), name="list"),
    path('my-tickets/', views.MyTicketListView.as_view(), name="my_list"),
    path('my-assigned-tickets/', views.MyAssignedTicketListView.as_view(), name="my_assigned_list"),
    path('<int:pk>/view/', views.TicketDetailView.as_view(), name="detail"),
    path('<int:pk>/edit/', views.TicketUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name="delete"),
    path('new/', views.TicketCreateView.as_view(), name="create"),
    path('<int:pk>/new-note/', views.TicketNoteUpdateView.as_view(), name="new_note"),
    path('<int:ticket>/resolved/', views.mark_ticket_resolved, name="ticket_resolved"),
    path('<int:ticket>/re-opened/', views.mark_ticket_active, name="ticket_reopened"),

    # feedback form
    path('feedback-form/new/', views.TicketCreateViewPopout.as_view(), name="bug_create"),
    path('feedback-form/new/application/<str:app>/', views.TicketCreateViewPopout.as_view(), name="bug_create"),
    path('feedback-form/<int:pk>/view/', views.TicketConfirmationTemplateView.as_view(), name="confirm"),

    # github views
    path('<int:pk>/create-github-issue/', views.create_github_issue, name="git_create"),
    # path('<int:pk>/resolved-github-issue/', views.resolve_github_issue, name="git_resolve"),
    # path('<int:pk>/reopen-github-issue/', views.reopen_github_issue, name="git_reopen"),

    # EMAIL #
    #########
    path('<int:ticket>/send-resolved-notification/', views.send_resolved_email, name="send_resolved_email"),

    # Files #
    #########
    path('<int:ticket>/file/new/', views.FileCreateView.as_view(), name="file_create"),
    path('<int:ticket>/file/<int:pk>/view', views.FileDetailView.as_view(), name="file_detail"),
    path('<int:ticket>/file/<int:pk>/edit', views.FileUpdateView.as_view(), name="file_update"),
    path('<int:ticket>/file/<int:pk>/delete', views.FileDeleteView.as_view(), name="file_delete"),
    path('<int:ticket>/add_generic_file/<str:type>/', views.add_generic_file, name="add_generic_file"),

    # follow up #
    #############
    path('<int:ticket>/follow-up/new/', views.FollowUpCreateView.as_view(), name="followup_create"),
    path('follow-up/<int:pk>/edit/', views.FollowUpUpdateView.as_view(), name="followup_edit"),
    path('follow-up/<int:pk>/delete/', views.FollowUpDeleteView.as_view(), name="followup_delete"),

    # Reports #
    ###########
    path('reports/finance/', views.FinanceReportListView.as_view(), name="finance_report"),
    path('reports/finance-spreadsheet/', views.finance_spreadsheet, name="finance_spreadsheet"),

]
