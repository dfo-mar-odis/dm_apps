from django.urls import reverse_lazy
from django.test import tag
from django.utils import timezone
from django.utils.translation import activate
from django.views.generic import CreateView, UpdateView, FormView

from shared_models.views import CommonUpdateView
from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from .. import views
from .. import models
from .. import utils
from faker import Faker

faker = Faker()


class TestTripRequestUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IndividualTripRequestFactory()
        self.instance_child = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_edit', args=(self.instance.pk, "my"))
        self.test_url1 = reverse_lazy('travel:request_edit', args=(self.instance_child.pk, "pop"))
        self.expected_template = 'travel/trip_request_form.html'
        self.expected_template1 = 'travel/trip_request_form_popout.html'

    @tag("travel", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripRequestUpdateView, views.CanModifyMixin)

    @tag("travel", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.instance.user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.instance_child.user)

    @tag("travel", "context")
    def test_context(self):
        context_vars = [
            "cost_field_list",
            "user_json",
            "conf_json",
            "help_text_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.instance.user)
        self.assert_presence_of_context_vars(self.test_url1, context_vars, user=self.instance_child.user)

    @tag("travel", "submit")
    def test_submit(self):
        data = FactoryFloor.IndividualTripRequestFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.instance.user)
        data = FactoryFloor.ChildTripRequestFactory.get_valid_data()
        self.assert_success_url(self.test_url1, data=data, user=self.instance_child.user)




class TestTripUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url0 = reverse_lazy('travel:trip_edit', kwargs={"pk": self.instance.pk, "type": "upcoming"})
        self.test_url1 = reverse_lazy('travel:trip_edit', kwargs={"pk": self.instance.pk, "type": "pop"})
        self.test_url2 = reverse_lazy('travel:trip_edit', kwargs={"pk": self.instance.pk, "type": "region-1"})
        self.expected_template = 'travel/trip_form.html'
        self.expected_template1 = 'travel/trip_form_popout.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("trip_update", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripUpdateView, CommonUpdateView)

    @tag("trip_update", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url0)
        self.assert_not_broken(self.test_url1)
        self.assert_not_broken(self.test_url2)
        self.assert_non_public_view(test_url=self.test_url0, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template, user=self.admin_user)

    @tag("trip_update", "context")
    def test_context(self):
        context_vars = [
            "help_text_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url0, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url1, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url2, context_vars, user=self.admin_user)

    @tag("trip_update", "submit")
    def test_submit(self):
        data = FactoryFloor.TripFactory.get_valid_data()
        self.assert_success_url(self.test_url0, data=data, user=self.admin_user)
        self.assert_success_url(self.test_url1, data=data, user=self.admin_user)
        self.assert_success_url(self.test_url2, data=data, user=self.admin_user)


class TestTripVerifyUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url = reverse_lazy('travel:trip_verify', kwargs={"pk": self.instance.pk, "region": 0, "adm": 0})
        self.expected_template = 'travel/trip_verification_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("travel", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripVerifyUpdateView, FormView)
        self.assert_inheritance(views.TripVerifyUpdateView, views.TravelAdminRequiredMixin)

    @tag("travel", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("travel", "context")
    def test_context(self):
        context_vars = [
            "object",
            "conf_field_list",
            "same_day_trips",
            "same_location_trips",
            "same_name_trips",
            "trip_subcategories",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)

    @tag("travel", "submit")
    def test_submit(self):
        data = FactoryFloor.TripFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)
        # check the trip status!! should be equal to 41 after form.save()
        self.instance = models.Conference.objects.get(id=self.instance.id)
        self.assertIs(self.instance.status_id, 41)


class TestDefaultReviewerUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DefaultReviewerFactory()
        self.test_url = reverse_lazy('travel:default_reviewer_edit', kwargs={"pk": self.instance.pk})
        self.admin_user = self.get_and_login_user(in_group="travel_admin")
        self.expected_template = 'travel/default_reviewer_form.html'

    @tag("default_reviewer_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.DefaultReviewerUpdateView, UpdateView)

    @tag("default_reviewer_edit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("default_reviewer_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.DefaultReviewerFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestTripRequestSubmitUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.reviewer = FactoryFloor.ReviewerFactory()
        self.instance = self.reviewer.trip_request
        self.user = self.instance.user
        self.test_url = reverse_lazy('travel:request_submit', args=(self.instance.pk, "my"))
        self.expected_template = 'travel/trip_request_submission_form.html'

    @tag("request_submit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestSubmitUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripRequestSubmitUpdateView, views.CanModifyMixin)

    @tag("request_submit", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("request_submit", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "triprequest",
            "child_field_list",
            "reviewer_field_list",
            "conf_field_list",
            "cost_field_list",
            "help_text_dict",
            "report_mode",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("request_submit", "submit")
    def test_submit(self):
        # ensure we are starting off with what we expect: no submission dates
        self.assertIsNone(self.instance.submitted)
        self.assertIsNone(self.instance.original_submission_date)
        self.assert_success_url(self.test_url, user=self.user)

        # after submitting the form, there should now be submission dates
        self.instance = models.TripRequest.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.submitted)
        self.assertIsNotNone(self.instance.original_submission_date)

        # run it a second time and now it should be unsubmitted, but the original submission date should still be there
        # the trick here is to ensure there is a reviewer on the request.
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.TripRequest.objects.get(pk=self.instance.pk)
        self.assertIsNone(self.instance.submitted)
        self.assertIsNotNone(self.instance.original_submission_date)

        # test that you cannot submit to a closed trip (ie. when not = 30 or 41)
        my_trip = self.instance.trip
        my_trip.status_id = [43, 31, 32][faker.pyint(0, 2)]
        my_trip.save()
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.TripRequest.objects.get(pk=self.instance.pk)
        self.assertIsNone(self.instance.submitted)
        self.assertIsNotNone(self.instance.original_submission_date)


class TestTripReviewProcessUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.user = self.get_and_login_user(in_group="travel_adm_admin")
        self.test_url = reverse_lazy('travel:trip_review_toggle', kwargs={"pk": self.instance.pk})
        self.expected_template = 'travel/trip_review_process_form.html'

    @tag("trip_review_toggle", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripReviewProcessUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripReviewProcessUpdateView, views.TravelADMAdminRequiredMixin)

    @tag("trip_review_toggle", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

        # if there is an inappropriate trip, we should get 302 response
        reviewed_trip = FactoryFloor.TripFactory(status_id=32)
        cancelled_trip = FactoryFloor.TripFactory(status_id=43)
        self.test_url1 = reverse_lazy('travel:trip_review_toggle', kwargs={"pk": reviewed_trip.pk})
        self.test_url2 = reverse_lazy('travel:trip_review_toggle', kwargs={"pk": cancelled_trip.pk})
        self.assert_non_public_view(test_url=self.test_url1, expected_code=302, user=self.user)
        self.assert_non_public_view(test_url=self.test_url2, expected_code=302, user=self.user)

    @tag("trip_review_toggle", "context")
    def test_context(self):
        context_vars = [
            "trip",
            "conf_field_list",
            "help_text_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("trip_review_toggle", "submit")
    def test_submit(self):
        # create a few reviewers so that it does not go straight to "reviewed" status
        FactoryFloor.TripReviewerFactory(trip=self.instance)
        FactoryFloor.TripReviewerFactory(trip=self.instance)
        FactoryFloor.TripReviewerFactory(trip=self.instance)
        # ensure we are starting off with what we expect: no submission dates
        self.assertIsNone(self.instance.review_start_date)
        self.assert_success_url(self.test_url, user=self.user)

        # after submitting the form, there should now be a review start date and the status should be updated
        self.instance = models.Conference.objects.get(pk=self.instance.pk)

        self.assertIsNotNone(self.instance.review_start_date)
        self.assertEqual(self.instance.status_id, 31)
        # run it a second time and now it should be unsubmitted, but the original submission date should still be there
        # the trick here is to ensure there is a reviewer on the request.
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.Conference.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.review_start_date)
        self.assertEqual(self.instance.status_id, 41)


class TestTripRequestReviewerUpdateView(CommonTest):
    def setUp(self):
        super().setUp()

        # actors
        self.tr = FactoryFloor.IndividualTripRequestFactory(submitted=timezone.now())
        self.reviewer1 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role_id=1, order=1)
        self.reviewer2 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role_id=5, order=2)
        self.reviewer3 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role_id=6, order=3)
        # start the review process and get set the first reviewer to "pending"
        utils.start_review_process(self.tr)
        utils.approval_seeker(self.tr, True)
        self.test_url1 = reverse_lazy('travel:tr_review_update', kwargs={"pk": self.reviewer1.pk})

        # there are two cases we will want to test. 1) an admin coming in to approve on behalf of and 2) a reviewer approving their own record

        # 2)

        self.expected_template = 'travel/reviewer_approval_form.html'

    @tag("tr_reviewer_update", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestReviewerUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripRequestReviewerUpdateView, views.AdminOrApproverRequiredMixin)

    @tag("tr_reviewer_update", "access")
    def test_view(self):
        self.assert_not_broken(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=self.reviewer1.user)

    @tag("tr_reviewer_update", "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "child_field_list",
            "reviewer_field_list",
            "conf_field_list",
            "cost_field_list",
            "help_text_dict",
            "report_mode",
            "trip",
            "triprequest",
        ]
        self.assert_presence_of_context_vars(self.test_url1, context_vars, user=self.reviewer1.user)

    @tag("tr_reviewer_update", "submit")
    def test_submit_approve(self):
        data_approve = {"comments": faker.catch_phrase(), "approved": True}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_approve)
        # the reviewer's status should now be set to approved
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status_id, 2)

    @tag("tr_reviewer_update", "submit")
    def test_submit_deny(self):
        data_deny = {"comments": faker.catch_phrase(), "approved": False}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_deny)
        # the reviewer's status should now be set to denied
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status_id, 3)

    @tag("tr_reviewer_update", "submit")
    def test_submit_changes(self):
        data_request_changes = {"comments": faker.catch_phrase(), "changes_requested": True}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_request_changes)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status_id, 1)
        self.assertEqual(rev1.trip_request.status_id, 16)

    @tag("tr_reviewer_update", "submit")
    def test_submit_save_draft(self):
        data_stay = {"comments": faker.catch_phrase(), "stay_on_page": True}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_stay)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status_id, 1)


class TestTripReviewerUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user(in_group="travel_adm_admin")
        self.reviewer = FactoryFloor.TripReviewerFactory(user=self.user)
        self.trip = self.reviewer.trip
        # the trip must be submitted for review
        self.start_review_url = reverse_lazy('travel:trip_review_toggle', kwargs={"pk": self.trip.pk})
        activate('en')
        # if a user is provided in the arg, log in with that user
        response = self.client.post(self.start_review_url)
        self.test_url = reverse_lazy('travel:trip_reviewer_update', kwargs={"pk": self.reviewer.pk})
        self.expected_template = 'travel/trip_reviewer_approval_form.html'

    @tag("trip_reviewer_update", 'type', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripReviewerUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripReviewerUpdateView, views.TravelADMAdminRequiredMixin)

    @tag("trip_reviewer_update", 'type', "access")
    def test_view(self):
        self.assert_not_broken(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("trip_reviewer_update", 'type', "context")
    def test_context(self):
        context_vars = [
            "conf_field_list",
            "reviewer_field_list",
            "report_mode",
            "trip",
            "adm_can_submit",
            "adm_tr_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)
        # TODO: NEED TO TEST WITH ADM REVIEWER AND MAKE SURE EXTRA FIELDS ARE PRESENT!!

    @tag("trip_reviewer_update", 'type', "submit")
    def test_submit(self):
        data = {"comments": faker.catch_phrase(), }  # for this form, as long as we are not "staying on page" it is considered approved
        self.assert_success_url(self.test_url, user=self.reviewer.user, data=data)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.TripReviewer.objects.get(pk=self.reviewer.pk)
        self.assertEqual(rev1.status_id, 26)

    @tag("trip_reviewer_update", 'type', "submit")
    def test_submit_save_only(self):
        data = {"comments": faker.catch_phrase(),
                "stay_on_page": True}  # for this form, as long as we are not "staying on page" it is considered approved
        self.assert_success_url(self.test_url, user=self.reviewer.user, data=data)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.TripReviewer.objects.get(pk=self.reviewer.pk)
        self.assertEqual(rev1.status_id, 25)

        # approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)
        #     changes_requested = forms.BooleanField(widget=forms.HiddenInput(), required=False)
        #     stay_on_page = forms.BooleanField(widget=forms.HiddenInput(), required=False)
        # todo: start the review process on the trip
        # todo: confirm that this is the active reviewer
        # todo: confirm that this is the active reviewer with status == pending
        # TODO: submit the form; approve --> check status
        # data = FactoryFloor.TripReviewerFactory.get_valid_data()
        # self.assert_success_url(self.test_url, data=data, user=self.user)

# TODO: TEST TRIP REQUEST REVIEWER UPDATE VIEW!!
# TODO: test the whole requesting changes peice
