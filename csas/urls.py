from django.urls import path
from . import views

app_name = 'csas'

urlpatterns = [
    # for home/index page
    path('',                                        views.IndexTemplateView.as_view(),    name="index"),
    path('index_meeting/',                          views.IndexMeetingView.as_view(),     name="index_met"),
    path('index_publication',                       views.IndexPublicationView.as_view(), name="index_pub"),

    # for Requests
    path('request/',                                views.RequestList.as_view(),          name="list_req"),
    path('request/reg/',                            views.RequestListReg.as_view(),       name="list_req_reg"),

    path('request/',                                views.RequestList.as_view(),          name="list_req_CSAS"),

    path('request/new/',                            views.RequestEntry.as_view(),         name="create_req"),
    path('request_CSAS/new/',                       views.RequestEntryCSAS.as_view(),     name="create_req_CSAS"),

    path('request/update/<int:pk>/',                views.RequestUpdate.as_view(),        name="update_req"),
    path('request/update/<int:pk>/<str:pop>/',      views.RequestUpdate.as_view(),        name="update_req"),
    path('request_CSAS/update/<int:pk>/',           views.RequestUpdateCSAS.as_view(),    name="update_req_CSAS"),
    path('request_CSAS/update/<int:pk>/<str:pop>/', views.RequestUpdateCSAS.as_view(),    name="update_req_CSAS"),

    path('request/details/<int:pk>/',               views.RequestDetails.as_view(),       name="details_req"),
    path('request_CSAS/details/<int:pk>/',          views.RequestDetailsCSAS.as_view(),   name="details_req_CSAS"),

    # for Meetings
    path('meeting/',                    views.MeetingList.as_view(),          name="list_met"),
    path('meeting/reg/',                views.MeetingListReg.as_view(),       name="list_met_reg"),
    path('meeting_DFO_participants/',   views.MeetingListDFOPars.as_view(),   name="list_met_DFO_pars"),
    path('meeting_other_participants/', views.MeetingListOtherPars.as_view(), name="list_met_other_pars"),

    path('meeting/new/',                                           views.MeetingEntry.as_view(),          name="create_met"),
    path('meeting_docs/new/<int:met_id>/<str:pop>/',               views.MeetingEntryDocs.as_view(),      name="create_met_doc"),
    path('meeting_docs/new/',                                      views.MeetingEntryDocs.as_view(),      name="create_met_doc"),
    path('meeting_DFO_participants/new/<int:met_id>/<str:pop>/',   views.MeetingEntryDFOPars.as_view(),   name="create_met_DFO_pars"),
    path('meeting_DFO_participants/new/',                          views.MeetingEntryDFOPars.as_view(),   name="create_met_DFO_pars"),
    path('meeting_other_participants/new/<int:met_id>/<str:pop>/', views.MeetingEntryOtherPars.as_view(), name="create_met_other_pars"),
    path('meeting_other_participants/new/',                        views.MeetingEntryOtherPars.as_view(), name="create_met_other_pars"),
    path('meeting_OM_costs/new/<int:met_id>/<str:pop>/',           views.MeetingEntryOMCosts.as_view(),   name="create_met_OM_costs"),
    path('meeting_OM_costs/new/',                                  views.MeetingEntryOMCosts.as_view(),   name="create_met_OM_costs"),
    path('meeting_media/new/<int:met_id>/<str:pop>/',              views.MeetingEntryMedia.as_view(),     name="create_met_media"),
    path('meeting_media/new/',                                     views.MeetingEntryMedia.as_view(),     name="create_met_media"),

    path('meeting/update/<int:pk>/<str:pop>/',                    views.MeetingUpdate.as_view(),          name="update_met"),
    path('meeting/update/<int:pk>/',                              views.MeetingUpdate.as_view(),          name="update_met"),
    path('meeting_docs/update/<int:pk>/<str:pop>/',               views.MeetingUpdateDocs.as_view(),      name="update_met_doc"),
    path('meeting_docs/update/<int:pk>/',                         views.MeetingUpdateDocs.as_view(),      name="update_met_doc"),
    path('meeting_DFO_participants/update/<int:pk>/<str:pop>/',   views.MeetingUpdateDFOPars.as_view(),   name="update_met_DFO_pars"),
    path('meeting_DFO_participants/update/<int:pk>/',             views.MeetingUpdateDFOPars.as_view(),   name="update_met_DFO_pars"),
    path('meeting_other_participants/update/<int:pk>/<str:pop>/', views.MeetingUpdateOtherPars.as_view(), name="update_met_other_pars"),
    path('meeting_other_participants/update/<int:pk>/',           views.MeetingUpdateOtherPars.as_view(), name="update_met_other_pars"),
    path('meeting_OM_costs/update/<int:pk>/<str:pop>/',           views.MeetingUpdateOMCosts.as_view(),   name="update_met_OM_costs"),
    path('meeting_OM_costs/update/<int:pk>/',                     views.MeetingUpdateOMCosts.as_view(),   name="update_met_OM_costs"),
    path('meeting_media/update/<int:pk>/<str:pop>/',              views.MeetingUpdateMedia.as_view(),     name="update_met_media"),
    path('meeting_media/update/<int:pk>/',                        views.MeetingUpdateMedia.as_view(),     name="update_met_media"),

    path('meeting/details/<int:pk>/',                    views.MeetingDetails.as_view(),          name="details_met"),
    path('meeting_docs/details/<int:pk>/',               views.MeetingDetailsDocs.as_view(),      name="details_met_docs"),
    path('meeting_DFO_participants/details/<int:pk>/',   views.MeetingDetailsDFOPars.as_view(),   name="details_met_DFO_pars"),
    path('meeting_other_participants/details/<int:pk>/', views.MeetingDetailsOtherPars.as_view(), name="details_met_other_pars"),
    path('meeting_OM_costs/details/<int:pk>/',           views.MeetingDetailsOMCosts.as_view(),   name="details_met_OM_costs"),
    path('meeting_media/details/<int:pk>/',              views.MeetingDetailsMedia.as_view(),     name="details_met_media"),

    # for Publications
    path('publication/',                                         views.PublicationList.as_view(),             name="list_pub"),
    path('publication/reg/',                                     views.PublicationListReg.as_view(),          name="list_pub_reg"),

    path('publication/new/',                                     views.PublicationEntry.as_view(),            name="create_pub"),
    path('publication_status/new/<int:pub_id>/<str:pop>/',       views.PublicationEntryStatus.as_view(),      name="create_pub_status"),
    path('publication_status/new/',                              views.PublicationEntryStatus.as_view(),      name="create_pub_status"),
    path('publication_trans_info/new/<int:pub_id>/<str:pop>/',   views.PublicationEntryTransInfo.as_view(),   name="create_pub_trans_info"),
    path('publication_trans_info/new/',                          views.PublicationEntryTransInfo.as_view(),   name="create_pub_trans_info"),
    path('publication_doc_location/new/<int:pub_id>/<str:pop>/', views.PublicationEntryDocLocation.as_view(), name="create_pub_doc_location"),
    path('publication_doc_location/new/',                        views.PublicationEntryDocLocation.as_view(), name="create_pub_doc_location"),
    path('publication_OM_costs/new/<int:pub_id>/<str:pop>/',     views.PublicationEntryOMCosts.as_view(),     name="create_pub_OM_costs"),
    path('publication_OM_costs/new/',                            views.PublicationEntryOMCosts.as_view(),     name="create_pub_OM_costs"),
    path('publication_comm_results/new/<int:pub_id>/<str:pop>/', views.PublicationEntryComResults.as_view(),  name="create_pub_com_results"),
    path('publication_comm_results/new/',                        views.PublicationEntryComResults.as_view(),  name="create_pub_com_results"),

    path('publication/update/<int:pk>/<str:pop>/',              views.PublicationUpdate.as_view(),            name="update_pub"),
    path('publication/update/<int:pk>/',                        views.PublicationUpdate.as_view(),            name="update_pub"),
    path('publication_status/update/<int:pk>/<str:pop>/',       views.PublicationUpdateStatus.as_view(),      name="update_pub_status"),
    path('publication_status/update/<int:pk>/',                 views.PublicationUpdateStatus.as_view(),      name="update_pub_status"),
    path('publication_trans_info/update/<int:pk>/<str:pop>/',   views.PublicationUpdateTransInfo.as_view(),   name="update_pub_trans_info"),
    path('publication_trans_info/update/<int:pk>/',             views.PublicationUpdateTransInfo.as_view(),   name="update_pub_trans_info"),
    path('publication_doc_location/update/<int:pk>/<str:pop>/', views.PublicationUpdateDocLocation.as_view(), name="update_pub_doc_location"),
    path('publication_doc_location/update/<int:pk>/',           views.PublicationUpdateDocLocation.as_view(), name="update_pub_doc_location"),
    path('publication_OM_costs/update/<int:pk>/<str:pop>/',     views.PublicationUpdateOMCosts.as_view(),     name="update_pub_OM_costs"),
    path('publication_OM_costs/update/<int:pk>/',               views.PublicationUpdateOMCosts.as_view(),     name="update_pub_OM_costs"),
    path('publication_com_results/update/<int:pk>/<str:pop>/',  views.PublicationUpdateComResults.as_view(),  name="update_pub_com_results"),
    path('publication_com_results/update/<int:pk>/',            views.PublicationUpdateComResults.as_view(),  name="update_pub_com_results"),

    path('publication/details/<int:pk>/',              views.PublicationDetails.as_view(),            name="details_pub"),
    path('publication_status/details/<int:pk>/',       views.PublicationDetailsStatus.as_view(),      name="details_pub_status"),
    path('publication_trans_info/details/<int:pk>/',   views.PublicationDetailsTransInfo.as_view(),   name="details_pub_trans_info"),
    path('publication_doc_location/details/<int:pk>/', views.PublicationDetailsDocLocation.as_view(), name="details_pub_doc_location"),
    path('publication_OM_costs/details/<int:pk>/',     views.PublicationDetailsOMCosts.as_view(),     name="details_pub_OM_costs"),
    path('publication_com_results/details/<int:pk>/',  views.PublicationDetailsComResults.as_view(),  name="details_pub_com_results"),

    # for Contacts
    path('contacts/',                              views.ContactList.as_view(),        name="list_con"),
    path('contacts/reg/',                          views.ContactListReg.as_view(),     name="list_con_reg"),
    path('contacts/new/',                          views.ContactEntry.as_view(),       name="create_con"),
    path('contacts/update/<int:pk>/<str:pop>/',    views.ContactUpdate.as_view(),      name="update_con"),
    path('contacts/update/<int:pk>/',              views.ContactUpdate.as_view(),      name="update_con"),
    path('contacts/details/<int:pk>/',             views.ContactDetails.as_view(),     name="details_con"),

    path('close/',                                 views.CloserTemplateView.as_view(), name="close_me"),
    # path('create/honorific/',                    views.HonorificView.as_view(),      name="create_coh"),
    path('create/language/',                       views.LanguageView.as_view(),       name="create_lan"),

    # --------------------------------------------------------------------------------------------- #
    # Lookup URLs
    # --------------------------------------------------------------------------------------------- #
    path('lookup/coh/',                    views.CohList.as_view(),       name="list_coh"),
    path('create/coh/',                    views.CreateCohView.as_view(), name="create_coh"),
    path('create/coh/<str:pop>/',          views.CreateCohView.as_view(), name="create_coh"),
    path('update/coh/<int:pk>/<str:pop>/', views.UpdateCohView.as_view(), name="update_coh"),

    path('lookup/stt/',                    views.SttList.as_view(),       name="list_stt"),
    path('create/stt/',                    views.CreateSttView.as_view(), name="create_stt"),
    path('create/stt/<str:pop>/',          views.CreateSttView.as_view(), name="create_stt"),
    path('update/stt/<int:pk>/<str:pop>/', views.UpdateSttView.as_view(), name="update_stt"),

    path('lookup/meq/',                    views.MeqList.as_view(),       name="list_meq"),
    path('create/meq/',                    views.CreateMeqView.as_view(), name="create_meq"),
    path('create/meq/<str:pop>/',          views.CreateMeqView.as_view(), name="create_meq"),
    path('update/meq/<int:pk>/<str:pop>/', views.UpdateMeqView.as_view(), name="update_meq"),

    path('lookup/loc/',                    views.LocList.as_view(),       name="list_loc"),
    path('create/loc/',                    views.CreateLocView.as_view(), name="create_loc"),
    path('create/loc/<str:pop>/',          views.CreateLocView.as_view(), name="create_loc"),
    path('update/loc/<int:pk>/<str:pop>/', views.UpdateLocView.as_view(), name="update_loc"),

    path('lookup/apt/',                    views.AptList.as_view(),       name="list_apt"),
    path('create/apt/',                    views.CreateAptView.as_view(), name="create_apt"),
    path('create/apt/<str:pop>/',          views.CreateAptView.as_view(), name="create_apt"),
    path('update/apt/<int:pk>/<str:pop>/', views.UpdateAptView.as_view(), name="update_apt"),

    path('lookup/scp/',                    views.ScpList.as_view(),       name="list_scp"),
    path('create/scp/',                    views.CreateScpView.as_view(), name="create_scp"),
    path('create/scp/<str:pop>/',          views.CreateScpView.as_view(), name="create_scp"),
    path('update/scp/<int:pk>/<str:pop>/', views.UpdateScpView.as_view(), name="update_scp"),

    # path('search/', views.SearchFormView.as_view(), name="sample_search"),
    # path('dataflow/', views.DataFlowTemplateView.as_view(), name ="dataflow" ),
]
