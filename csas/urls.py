from django.urls import path
from . import views

app_name = 'csas'

urlpatterns = [
    # for home/index page
    path('',                                    views.IndexTemplateView.as_view(),  name="index"),

    # for Requests
    path('request/',                            views.RequestList.as_view(),        name="list_req"),
    path('request/new/',                        views.RequestEntry.as_view(),       name="create_req"),
    path('request/update/<int:pk>/',            views.RequestUpdate.as_view(),      name="update_req"),
    path('request/update/<int:pk>/<str:pop>/',  views.RequestUpdate.as_view(),      name="update_req"),
    path('request/details/<int:pk>/',           views.RequestDetails.as_view(),     name="details_req"),

    # for Meetings
    path('meeting/',                            views.MeetingList.as_view(),        name="list_met"),
    path('meeting/new/',                        views.MeetingEntry.as_view(),       name="create_met"),
    path('meeting/update/<int:pk>/',            views.MeetingUpdate.as_view(),      name="update_met"),
    path('meeting/details/<int:pk>/',           views.MeetingDetails.as_view(),     name="details_met"),

    # for Publications
    path('publication/',                        views.PublicationList.as_view(),    name="list_pub"),
    path('publication/new/',                    views.PublicationEntry.as_view(),   name="create_pub"),
    path('publication/update/<int:pk>/',        views.PublicationUpdate.as_view(),  name="update_pub"),
    path('publication/details/<int:pk>/',       views.PublicationDetails.as_view(), name="details_pub"),

    # for Contacts
    path('contacts/',                           views.ContactList.as_view(),       name="list_con"),
    path('contacts/new/',                       views.ContactEntry.as_view(),      name="create_con"),
    path('contacts/update/<int:pk>/<str:pop>/', views.ContactUpdate.as_view(),     name="update_con"),
    path('contacts/update/<int:pk>/',           views.ContactUpdate.as_view(),     name="update_con"),
    path('contacts/details/<int:pk>/',          views.ContactDetails.as_view(),    name="details_con"),

    path('close/',                              views.CloserTemplateView.as_view(), name="close_me"),
    path('create/honorific/',                   views.HonorificView.as_view(),      name="create_coh"),
    path('create/language/',                    views.LanguageView.as_view(),       name="create_lan")

    # path('search/', views.SearchFormView.as_view(), name="sample_search"),
    # path('dataflow/', views.DataFlowTemplateView.as_view(), name ="dataflow" ),
]
