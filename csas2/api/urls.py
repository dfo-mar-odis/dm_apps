from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'requests', views.CSASRequestViewSet)

router.register(r'meetings', views.MeetingViewSet)
router.register(r'notes', views.MeetingNoteViewSet)
router.register(r'invitees', views.InviteeViewSet)
router.register(r'resources', views.MeetingResourceViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'people', views.PersonViewSet)


urlpatterns = [
    path("csas/", include(router.urls)),  # tested
    path("csas/user/", views.CurrentUserAPIView.as_view(), name="csas-current-user"),

    path("csas/meta/models/meeting/", views.MeetingModelMetaAPIView.as_view(), name="event-model-meta"),
    path("csas/meta/models/note/", views.NoteModelMetaAPIView.as_view(), name="note-model-meta"),
    path("csas/meta/models/invitee/", views.InviteeModelMetaAPIView.as_view(), name="invitee-model-meta"),
    path("csas/meta/models/person/", views.PersonModelMetaAPIView.as_view(), name="person-model-meta"),
    path("csas/meta/models/resource/", views.ResourceModelMetaAPIView.as_view(), name="resource-model-meta"),
    path("csas/invitees/<int:pk>/invitation/", views.InviteeSendInvitationAPIView.as_view(), name="invitee-send-invitation"),
    # path("csas/documents/<int:pk>/toggle-meeting-linkage/", views.DocumentMeetingLinkageAPIView.as_view(), name="document-meeting-lnka"),
]