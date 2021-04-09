import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from dm_apps.emails import Email

from_email = settings.SITE_FROM_EMAIL

request_field_list = [
    'fiscal_year',
    'section',
    'created_by',
    'trip',
]

trip_field_list = [
    'fiscal_year',
    'name',
    'nom',
    'lead',
    'is_adm_approval_required',
    'location',
    'start_date',
    'end_date',
]


class NewTripEmail(Email):
    email_template_path = 'travel/emails/email_new_event.html'
    subject_en = 'Trip verification is needed'
    subject_fr = "Une vérification du voyage est nécessaire"

    def get_recipient_list(self):
        if self.instance.is_adm_approval_required:
            return [user.email for user in User.objects.filter(groups__name="travel_adm_admin")]
        else:
            adm_admins = [user.id for user in User.objects.filter(groups__name="travel_adm_admin")]
            return [user.email for user in User.objects.filter(groups__name="travel_admin").filter(~Q(id__in=adm_admins))]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'event': self.instance, 'field_list': trip_field_list})
        return context


class RDGReviewAwaitingEmail(Email):
    email_template_path = 'travel/emails/email_admin_awaiting_approval.html'

    def get_subject_en(self):
        return 'A trip request is awaiting {} approval'.format(self.reviewer.get_role_display())

    def get_recipient_list(self):
        return [user.email for user in User.objects.filter(groups__name="travel_admin")]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'reviewer': self.reviewer, 'triprequest': self.instance, 'field_list': request_field_list})
        return context

    def __init__(self, request, instance=None, reviewer=None):
        super().__init__(request)
        self.request = request
        self.instance = instance
        self.reviewer = reviewer


class ReviewAwaitingEmail(Email):
    email_template_path = 'travel/emails/email_awaiting_review.html'

    def get_subject_en(self):
        return 'A LATE trip request is awaiting your review' if self.instance.is_late_request else 'A trip request is awaiting your review'

    def get_subject_fr(self):
        return 'Une demande de voyage TARDIVE attend votre examen' if self.instance.is_late_request else 'Une demande de voyage attend votre examenw'

    def get_recipient_list(self):
        return [self.reviewer.user.email, ]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'reviewer': self.reviewer, 'triprequest': self.instance, 'field_list': request_field_list})
        return context

    def __init__(self, request, instance=None, reviewer=None):
        super().__init__(request)
        self.request = request
        self.instance = instance
        self.reviewer = reviewer


class TripReviewAwaitingEmail(Email):
    email_template_path = 'travel/emails/email_awaiting_trip_review.html'
    subject_en = "A trip is awaiting your review"
    subject_fr = "un voyage attend votre avis"

    def get_recipient_list(self):
        return [self.reviewer.user.email, ]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'reviewer': self.reviewer, 'trip': self.instance, 'field_list': trip_field_list})
        return context

    def __init__(self, request, instance=None, reviewer=None):
        super().__init__(request)
        self.request = request
        self.instance = instance
        self.reviewer = reviewer


class ChangesRequestedEmail(Email):
    email_template_path = 'travel/emails/email_changes_requested.html'
    subject_en = "Changes to your trip request are required"
    subject_fr = "des modifications à votre demande de voyage sont nécessaires"

    def get_recipient_list(self):
        return [self.instance.created_by.email, ]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'triprequest': self.instance, 'field_list': request_field_list})
        return context


class StatusUpdateEmail(Email):
    email_template_path = 'travel/emails/email_status_update.html'

    def get_subject_en(self):
        return 'Your trip request has been ' + str(self.instance.get_status_display())

    def get_subject_fr(self):
        return "Votre demande de voyage a été " + str(self.instance.get_status_display())

    def get_recipient_list(self):
        to_list = [self.instance.created_by.email, ]
        to_list.extend([t.email for t in self.instance.travellers.all()])
        return to_list

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'triprequest': self.instance, 'field_list': request_field_list})
        return context


class RemovedTravellerEmail(Email):
    email_template_path = 'travel/emails/email_traveller_removed.html'
    subject_en = 'You have been removed from a request'
    subject_fr = "Vous avez été retiré d'une demande"

    def get_recipient_list(self):
        return [self.instance.email, ]


class TripCostWarningEmail(Email):
    email_template_path = 'travel/emails/email_trip_cost_warning.html'
    subject_en = '*** Trip cost warning'
    subject_fr = "Avertissement de coût de voyage ***"

    def get_recipient_list(self):
        travel_admin_list = [user.email for user in User.objects.filter(groups__name="travel_admin")]
        travel_admin_list.append("DFO.ScienceTravel-VoyagesSciences.MPO@dfo-mpo.gc.ca")
        return travel_admin_list

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'trip': self.instance, 'field_list': trip_field_list})
        return context


class TripReviewEmail(Email):
    email_template_path = 'travel/emails/trip_review.html'
    subject_en = 'ADM trip review has commenced'
    subject_fr = "L'examen de voyage par le SMA a commencé"

    def get_recipient_list(self):
        return [self.recip]

    def get_context_data(self):
        context = super().get_context_data()
        context.update({'due_date': timezone.now() + datetime.timedelta(days=7)})
        return context

    def __init__(self, request, instance=None, recip=None):
        super().__init__(request)
        self.request = request
        self.instance = instance
        self.recip = recip
