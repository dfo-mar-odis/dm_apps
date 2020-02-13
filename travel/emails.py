from django.contrib.auth.models import User
from django.template import loader

from_email = 'DoNotReply@DMApps.com'

request_field_list = [
    'fiscal_year',
    'section',
    'user',
    'trip',
    'destination',
    'start_date',
    'end_date',
]

trip_field_list = [
    'fiscal_year',
    'name',
    'nom',
    'is_adm_approval_required',
    'location',
    'start_date',
    'end_date',
]


class NewTripEmail:
    def __init__(self, event):
        self.event = event
        self.subject = 'Somebody created a new trip'
        self.message = self.load_html_template()
        self.from_email = from_email
        self.to_list = [user.email for user in User.objects.filter(groups__name="travel_admin")]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self):
        t = loader.get_template('travel/email_new_event.html')
        field_list = trip_field_list
        context = {'event': self.event, 'field_list': field_list}
        rendered = t.render(context)
        return rendered


class AdminApprovalAwaitingEmail:
    def __init__(self, trip_request):
        self.subject = 'A trip request is awaiting {} approval'.format(trip_request.current_reviewer.role)
        self.message = self.load_html_template(trip_request)
        self.from_email = from_email
        self.to_list = [user.email for user in User.objects.filter(groups__name="travel_admin")]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, trip_request):
        t = loader.get_template('travel/email_admin_awaiting_approval.html')

        field_list = request_field_list

        context = {'triprequest': trip_request, 'field_list': field_list}
        rendered = t.render(context)
        return rendered


class ReviewAwaitingEmail:
    def __init__(self, trip_request_object, reviewer_object):
        self.subject = 'A trip request is awaiting your review - un voyage attend votre avis'
        self.message = self.load_html_template(trip_request_object, reviewer_object)
        self.from_email = from_email
        self.to_list = [reviewer_object.user.email, ]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, trip_request_object, reviewer_object):
        t = loader.get_template('travel/email_awaiting_review.html')

        field_list = request_field_list

        context = {'reviewer': reviewer_object, 'triprequest': trip_request_object, 'field_list': field_list}
        rendered = t.render(context)
        return rendered


class ChangesRequestedEmail:
    def __init__(self, trip_request_object):
        self.subject = 'Changes to your trip request are required - des modifications à votre demande de voyage sont nécessaires'
        self.message = self.load_html_template(trip_request_object)
        self.from_email = from_email
        self.to_list = [trip_request_object.user.email, ]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, trip_request_object):
        t = loader.get_template('travel/email_changes_requested.html')

        field_list = request_field_list

        context = {'triprequest': trip_request_object, 'field_list': field_list}
        rendered = t.render(context)
        return rendered


class StatusUpdateEmail:
    def __init__(self, trip_request_object):
        self.subject = 'Your trip request has been ' + str(trip_request_object.status.name) + " - Votre demande de voyage a été " + str(
            trip_request_object.status.nom)
        self.message = self.load_html_template(trip_request_object)
        self.from_email = from_email
        self.to_list = [trip_request_object.user.email, ]

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, trip_request_object):
        t = loader.get_template('travel/email_status_update.html')

        field_list = request_field_list

        context = {'triprequest': trip_request_object, 'field_list': field_list}
        rendered = t.render(context)
        return rendered


class TripCostWarningEmail:

    def __init__(self, trip):

        self.subject = '*** Trip cost warning / Avertissement de coût de voyage ***'
        self.message = self.load_html_template(trip)
        self.from_email = from_email

        travel_admin_list = [user.email for user in User.objects.filter(groups__name="travel_admin")]
        travel_admin_list.append("DFO.ScienceTravel-VoyagesSciences.MPO@dfo-mpo.gc.ca")
        self.to_list = travel_admin_list

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)

    def load_html_template(self, trip_request_object):
        t = loader.get_template('travel/email_trip_cost_warning.html')

        field_list = trip_field_list

        context = {'trip': trip_request_object, 'field_list': field_list}
        rendered = t.render(context)
        return rendered
