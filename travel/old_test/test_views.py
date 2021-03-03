from datetime import timedelta

from django.contrib.auth.models import Group
from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate
from django.views.generic import FormView, CreateView, UpdateView
from faker import Faker

from shared_models.test.SharedModelsFactoryFloor import SectionFactory, RegionFactory
from shared_models.views import CommonFilterView, CommonDetailView, CommonListView, CommonUpdateView, CommonCreateView, CommonDeleteView
from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from .. import views, models, utils

faker = Faker()


###########################################################################################
# Index View is a bit different from most views as it is basically just a landing page
###########################################################################################


class IndividualTripRequestCreate(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres
        self.trip_request = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_new', args=("my",))
        self.expected_template = 'travel/trip_request_form.html'

    @tag("travel", 'create', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripCreateView, CommonCreateView)
        self.assert_inheritance(views.TripCreateView, views.TravelAccessRequiredMixin)

    @tag("trip_request", 'create', 'response')
    def test_access(self):
        # only logged in users can access the landing
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("trip_request", 'create', "context")
    def test_context(self):
        context_vars = [
            "user_json",
            "conf_json",
            "help_text_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

    @tag("trip_request", 'create', "submit")
    def test_submit(self):
        data = FactoryFloor.IndividualTripRequestFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data)
        # TODO: now we will want to make sense that the reviewers make sense... adm vs. non adm.. regional ppl etc


class IndividualTripRequestDelete(CommonTest):
    def setUp(self):
        super().setUp()
        self.tr = FactoryFloor.IndividualTripRequestFactory()
        self.tr1 = FactoryFloor.ChildTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_delete', args=(self.tr.pk, "my"))
        self.test_url1 = reverse_lazy('travel:request_delete', args=(self.tr1.pk, "pop"))
        self.expected_template = 'travel/confirm_delete.html'
        self.expected_template1 = 'shared_models/generic_popout_form.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("trip_request", 'delete', "view")
    def test_view_class(self):
        # make sure the view is inheriting from CanModify Mixin
        self.assert_inheritance(views.TripRequestDeleteView, views.CanModifyMixin)
        self.assert_inheritance(views.TripRequestDeleteView, CommonDeleteView)

    @tag("trip_request", 'delete', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template1, user=self.admin_user)

    @tag("trip_request", 'delete', "submit")
    def test_submit(self):
        # use an admin user because they should always be able to delete
        self.assert_success_url(self.test_url, user=self.admin_user)
        # ensure the user is deleted
        self.assertEqual(models.TripRequest.objects.filter(pk=self.tr.pk).count(), 0)

    @tag("trip_request", 'delete', "submit")
    def test_submit_pop(self):
        # use an admin user because they should always be able to delete
        self.assert_success_url(self.test_url1, user=self.admin_user)
        # ensure the user is deleted
        self.assertEqual(models.TripRequest.objects.filter(pk=self.tr1.pk).count(), 0)


class TestDefaultReviewerCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:default_reviewer_new')
        self.admin_user = self.get_and_login_user(in_group="travel_admin")
        self.expected_template = 'travel/default_reviewer_form.html'

    @tag("default_reviewer_new", 'create', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DefaultReviewerCreateView, CreateView)

    @tag("default_reviewer_new", 'create', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("default_reviewer_new", 'create', "submit")
    def test_submit(self):
        data = FactoryFloor.DefaultReviewerFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)

        # check if a section reviewer is added correctly to a trip request
        my_section = SectionFactory()
        my_reviewer = FactoryFloor.DefaultReviewerFactory()
        my_reviewer.sections.add(my_section)
        my_tr = FactoryFloor.IndividualTripRequestFactory(section=my_section)
        utils.get_tr_reviewers(my_tr)
        self.assertIn(my_reviewer.user, [r.user for r in my_tr.reviewers.all()])

        # check if a branch reviewer is added correctly to a trip request
        my_branch = my_section.division.branch
        my_reviewer = FactoryFloor.DefaultReviewerFactory()
        my_reviewer.branches.add(my_branch)
        my_tr = FactoryFloor.IndividualTripRequestFactory(section=my_section)
        utils.get_tr_reviewers(my_tr)
        self.assertIn(my_reviewer.user, [r.user for r in my_tr.reviewers.all()])


class TestDefaultReviewerListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:default_reviewer_list')
        self.expected_template = 'travel/default_reviewer_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("default_reviewer_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.DefaultReviewerListView, CommonListView)

    @tag("default_reviewer_list", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("default_reviewer_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "random_object",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, self.admin_user)


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
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("default_reviewer_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.DefaultReviewerFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.admin_user)


class TestIndexView(CommonTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('travel:index')
        self.expected_template = 'travel/index/index.html'

    # Users should be able to view the travel index page corresponding to the travel/index.html template, in French
    @tag("index")
    def test_access(self):
        # only logged in users can access the landing
        super().assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # The index view should return a context to be used on the index.html template
    # this should consist of a "Sections" dictionary containing sub-sections

    @tag("index", "context")
    def test_context(self):
        context_vars = [
            "user_trip_requests",

            "tr_reviews_waiting",
            "trip_reviews_waiting",
            "reviews_waiting",
            "is_reviewer",
            "is_tr_reviewer",
            "is_trip_reviewer",
            "is_admin",
            "is_adm_admin",
            "tab_dict",

            "processes",
            "information_sections",
            "faqs",
            "refs",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

        activate('en')
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        # a regular user should not be an admin or a reviewer
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_reviewer"], False)

        # if a regular user is also a reviewer, the 'is_reviewer' var should be true
        FactoryFloor.ReviewerFactory(user=reg_user)
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_reviewer"], True)

        # an admin user should be identified as such by the `is_admin` var in the template
        self.client.logout()
        admin_user = self.get_and_login_user(in_group="travel_admin")
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], True)

        # an adm admin user should be identified as such by the `is_adm_admin` var in the template
        self.client.logout()
        admin_user = self.get_and_login_user(in_group="travel_adm_admin")
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_adm_admin"], True)


class TestTripCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:trip_new', kwargs={"type": "upcoming"})
        self.test_url2 = reverse_lazy('travel:trip_new', kwargs={"type": "pop"}) + "?pop=true"

        self.expected_template = 'travel/trip_form.html'
        self.expected_template2 = 'travel/trip_form_popout.html'

    @tag("travel", 'create', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripCreateView, CommonCreateView)

    @tag("travel", 'create', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url2)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template2)

    @tag("travel", 'create', "context")
    def test_context(self):
        context_vars = [
            "help_text_dict",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)
        self.assert_presence_of_context_vars(self.test_url2, context_vars)

    @tag("travel", 'create', "submit")
    def test_submit(self):
        self.assert_success_url(self.test_url, data=FactoryFloor.TripFactory.get_valid_data())
        self.assert_success_url(self.test_url2, data=FactoryFloor.TripFactory.get_valid_data())


class TestTripDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance0 = FactoryFloor.TripFactory()
        self.instance1 = FactoryFloor.TripFactory()
        self.instance2 = FactoryFloor.TripFactory(lead=RegionFactory())
        self.instance3 = FactoryFloor.TripFactory(is_adm_approval_required=True)
        self.test_url0 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance0.pk, "type": "adm-hit-list"})
        self.test_url1 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance1.pk, "type": "region-1"})
        self.test_url2 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance2.pk, "type": "back_to_verify"})
        self.test_url3 = reverse_lazy('travel:trip_delete', kwargs={"pk": self.instance3.pk, "type": "all"})
        self.expected_template = 'travel/confirm_delete.html'

    @tag("trip_delete", 'delete', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripDeleteView, CommonDeleteView)

    @tag("trip_delete", 'delete', "access")
    def test_view(self):
        self.assert_good_response(self.test_url0)
        self.assert_good_response(self.test_url1)
        self.assert_good_response(self.test_url2)
        self.assert_good_response(self.test_url3)
        # TODO: do some more elaborate testing here!!
        my_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_non_public_view(test_url=self.test_url0, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template, user=my_user)
        self.assert_non_public_view(test_url=self.test_url3, expected_template=self.expected_template, user=my_user)

    @tag("trip_delete", 'delete', "submit")
    def test_submit(self):
        my_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_success_url(self.test_url0, user=my_user)
        self.assert_success_url(self.test_url1, user=my_user)
        self.assert_success_url(self.test_url2, user=my_user)
        self.assert_success_url(self.test_url3, user=my_user)

        # for delete views...
        self.assertEqual(models.Trip.objects.filter(pk=self.instance0.pk).count(), 0)
        self.assertEqual(models.Trip.objects.filter(pk=self.instance1.pk).count(), 0)
        self.assertEqual(models.Trip.objects.filter(pk=self.instance2.pk).count(), 0)
        self.assertEqual(models.Trip.objects.filter(pk=self.instance3.pk).count(), 0)


class TestTripDetailView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url0 = reverse_lazy('travel:trip_detail', kwargs={"pk": self.instance.pk, "type": "upcoming"})
        self.test_url1 = reverse_lazy('travel:trip_detail', kwargs={"pk": self.instance.pk, "type": "region-1"})
        self.expected_template = 'travel/trip_detail.html'
        self.user = self.get_and_login_user(in_group="travel_admin")

    @tag("travel", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripDetailView, CommonDetailView)

    @tag("travel", 'detail', "access")
    def test_view(self):
        self.assert_good_response(self.test_url0)
        self.assert_good_response(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url0, expected_template=self.expected_template, user=self.user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=self.user)

    @tag("travel", 'detail', "context")
    def test_context(self):
        context_vars = [
            "conf_field_list",
            "reviewer_field_list",
            "is_adm_admin",
            "trip",
        ]
        self.assert_presence_of_context_vars(self.test_url0, context_vars)
        self.assert_presence_of_context_vars(self.test_url1, context_vars)


class TestTripListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url2 = reverse_lazy('travel:trip_list', kwargs={"type": "upcoming"})  # should be accessible by anyone
        self.test_url3 = reverse_lazy('travel:trip_list', kwargs={"type": "adm-hit-list"})
        self.test_url1 = reverse_lazy('travel:trip_list', kwargs={"type": "all"})
        self.expected_template = 'travel/trip_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")
        # in order for this to work, we have to make sure there is a trip obj in the db
        FactoryFloor.TripFactory()

    @tag("trip_list", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripListView, CommonFilterView)
        self.assert_inheritance(views.TripListView, views.TravelAccessRequiredMixin)

    @tag("trip_list", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url2)
        self.assert_good_response(self.test_url3)
        self.assert_good_response(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template)
        self.assert_non_public_view(test_url=self.test_url3, expected_template=self.expected_template, user=self.admin_user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=self.admin_user)

    @tag("trip_list", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "is_admin",
        ]
        self.assert_presence_of_context_vars(self.test_url2, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url3, context_vars, user=self.admin_user)
        self.assert_presence_of_context_vars(self.test_url1, context_vars, user=self.admin_user)


class TestTripRequestReviewerUpdateView(CommonTest):
    def setUp(self):
        super().setUp()

        # actors
        self.tr = FactoryFloor.IndividualTripRequestFactory(submitted=timezone.now())
        self.reviewer1 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role=1, order=1)
        self.reviewer2 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role=5, order=2)
        self.reviewer3 = FactoryFloor.ReviewerFactory(trip_request=self.tr, role=6, order=3)
        # start the review process and get set the first reviewer to "pending"
        utils.start_request_review_process(self.tr)
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
        self.assert_good_response(self.test_url1)
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
        self.assertEqual(rev1.status, 2)

    @tag("tr_reviewer_update", "submit")
    def test_submit_deny(self):
        data_deny = {"comments": faker.catch_phrase(), "approved": False}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_deny)
        # the reviewer's status should now be set to denied
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status, 3)

    @tag("tr_reviewer_update", "submit")
    def test_submit_changes(self):
        data_request_changes = {"comments": faker.catch_phrase(), "changes_requested": True}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_request_changes)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status, 1)
        self.assertEqual(rev1.trip_request.status, 16)

    @tag("tr_reviewer_update", "submit")
    def test_submit_save_draft(self):
        data_stay = {"comments": faker.catch_phrase(), "stay_on_page": True}
        self.assert_success_url(self.test_url1, user=self.reviewer1.user, data=data_stay)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.Reviewer.objects.get(pk=self.reviewer1.pk)
        self.assertEqual(rev1.status, 1)


class TestTripRequestSubmitUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.reviewer = FactoryFloor.ReviewerFactory()
        self.instance = self.reviewer.request
        self.user = self.instance.user
        self.test_url = reverse_lazy('travel:request_submit', args=(self.instance.pk, "my"))
        self.expected_template = 'travel/trip_request_submission_form.html'

    @tag("request_submit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestSubmitUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripRequestSubmitUpdateView, views.CanModifyMixin)

    @tag("request_submit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
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

        # test that you when submitting to a trip that is passed the submission deadline, the NCR Travel coordinator
        # should be the first reviewer on the request

        ## create the ncr travel coordinator
        ncr_user = self.get_and_login_user(in_group="travel_adm_admin")
        ncr_coordinator = models.DefaultReviewer.objects.create(user=ncr_user)
        ncr_coordinator.reviewer_roles.add(3)

        ## configure trip to be past eligibility deadline
        my_trip = self.instance.trip
        my_trip.is_adm_approval_required = True
        my_trip.date_eligible_for_adm_review = timezone.now() - timedelta(days=2)
        my_trip.save()
        self.instance = models.TripRequest.objects.get(pk=self.instance.pk)

        ## make sure the TR is considered as late
        self.assertTrue(self.instance.is_late_request)

        ## submit the form
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.TripRequest.objects.get(pk=self.instance.pk)

        ## ensure that it is still labelled at late
        self.assertTrue(self.instance.is_late_request)
        print(self.instance.reviewers.first())
        self.assertEqual(self.instance.reviewers.first().user, ncr_user)


class TestTripRequestUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IndividualTripRequestFactory()
        self.instance_child = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_edit', args=(self.instance.pk,))
        self.expected_template = 'travel/trip_request_form.html'
        self.expected_template1 = 'travel/trip_request_form_popout.html'

    @tag("travel", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TripRequestUpdateView, views.CanModifyMixin)

    @tag("travel", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url1)
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
        # TODO:
        # test that you when submitting to a trip that is passed the submission deadline, a late justification is required
        # also one this is submitted, the NCR Travel coordinator should be the first reviewer on the request

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
        self.assert_good_response(self.test_url)
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
        self.assertEqual(rev1.status, 26)

    @tag("trip_reviewer_update", 'type', "submit")
    def test_submit_save_only(self):
        data = {"comments": faker.catch_phrase(),
                "stay_on_page": True}  # for this form, as long as we are not "staying on page" it is considered approved
        self.assert_success_url(self.test_url, user=self.reviewer.user, data=data)
        # the reviewer's status should now be set to changes_requested
        rev1 = models.TripReviewer.objects.get(pk=self.reviewer.pk)
        self.assertEqual(rev1.status, 25)

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
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

        # if there is an inappropriate trip, we should get 302 response
        cancelled_trip = FactoryFloor.TripFactory(status=43)
        self.test_url = reverse_lazy('travel:trip_review_toggle', kwargs={"pk": cancelled_trip.pk})
        self.assert_non_public_view(test_url=self.test_url, expected_code=302, user=self.user)

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
        r1 = FactoryFloor.TripReviewerFactory(trip=self.instance, order=1)
        r2 = FactoryFloor.TripReviewerFactory(trip=self.instance, order=2)
        r3 = FactoryFloor.TripReviewerFactory(trip=self.instance, order=3)
        # ensure we are starting off with what we expect: no submission dates
        self.assertIsNone(self.instance.review_start_date)
        self.assert_success_url(self.test_url, user=self.user)

        # after submitting the form, there should now be a review start date and the status should be updated
        self.instance = models.Trip.objects.get(pk=self.instance.pk)

        self.assertIsNotNone(self.instance.review_start_date)
        self.assertEqual(self.instance.status, 31)
        # run it a second time and now it should be unsubmitted, but the original submission date should still be there
        # the trick here is to ensure there is a reviewer on the request.
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.Trip.objects.get(pk=self.instance.pk)
        self.assertIsNotNone(self.instance.review_start_date)
        self.assertEqual(self.instance.status, 41)

        # now let's say the trip is reviewed..
        self.instance.status = 32
        self.instance.save()
        self.assertEqual(self.instance.status, 32)
        # let's add a reviewer comment and set the status to `complete`
        r1.comments = "good!"
        r2.comments = "trip!"
        r3.comments = "yayy!"
        r1.status = 26
        r2.status = 26
        r3.status = 26
        r1.save()
        r2.save()
        r3.save()
        self.assertEqual(r1.status, 26)
        self.assertEqual(r2.status, 26)
        self.assertEqual(r3.status, 26)


        # run it a second time and now the trip review process should be reset. The trip should still be under review and only the reviewer
        # statuses should be affected
        self.assert_success_url(self.test_url, user=self.user)
        self.instance = models.Trip.objects.get(pk=self.instance.pk)
        self.assertEqual(self.instance.status, 31)

        reviewer_ids = [r1.id, r2.id, r3.id]
        for id in reviewer_ids:
            r = models.TripReviewer.objects.get(pk=id)
            if r.order == 1:
                self.assertEqual(r.status, 25)
            else:
                self.assertEqual(r.status, 24)
            self.assertIsNotNone(r.comments)

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
        self.assert_good_response(self.test_url0)
        self.assert_good_response(self.test_url1)
        self.assert_good_response(self.test_url2)
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


class TestTripVerificationListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()
        self.test_url = reverse_lazy('travel:admin_trip_verification_list', kwargs={"region": 0, "adm": 0})
        self.expected_template = 'travel/trip_verification_list.html'
        self.admin_user = self.get_and_login_user(in_group="travel_admin")

    @tag("travel", 'list', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripVerificationListView, CommonListView)
        self.assert_inheritance(views.TripVerificationListView, views.TravelAdminRequiredMixin)

    @tag("travel", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        admin_user = self.get_and_login_user(in_group="travel_admin")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.admin_user)

    @tag("travel", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.admin_user)


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
        self.assert_good_response(self.test_url)
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
        self.instance = models.Trip.objects.get(id=self.instance.id)
        self.assertIs(self.instance.status, 41)


class TestUserListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('travel:user_list')
        self.test_url1 = reverse_lazy('travel:user_list', args=[1])
        self.expected_template = 'travel/user_list.html'
        self.user = self.get_and_login_user(in_group="travel_adm_admin")

    @tag("User", "user_list", "view")
    def test_view_class(self):
        self.assert_inheritance(views.UserListView, CommonFilterView)

    @tag("User", "user_list", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url1)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_non_public_view(test_url=self.test_url1, expected_template=self.expected_template, user=self.user)

    @tag("User", "user_list", "context")
    def test_context(self):
        context_vars = [
            "admin_group",
            "adm_admin_group",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)

    @tag("User", "user_list", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("travel:user_list", f"/en/travel-plans/settings/users/")


class TestUserToggleView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.UserFactory()
        self.test_url = reverse_lazy('travel:toggle_user', args=[self.instance.pk, 'admin'])
        self.test_url1 = reverse_lazy('travel:toggle_user', args=[self.instance.pk, 'adm_admin'])
        self.user = self.get_and_login_user(in_group="travel_adm_admin")

    @tag("UserToggle", "toggle_user", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url1)

        self.assert_non_public_view(test_url=self.test_url, user=self.user, expected_code=302)
        self.assert_non_public_view(test_url=self.test_url1, user=self.user, expected_code=302)

    @tag("UserToggle", "toggle_user", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("travel:toggle_user", f"/en/travel-plans/settings/user/{self.instance.pk}/toggle/{'admin'}/",
                                [self.instance.pk, 'admin'])

    @tag("UserToggle", "toggle_user", "function")
    def test_view_function(self):
        admin_group = Group.objects.get(pk=33)
        adm_admin_group = Group.objects.get(pk=36)

        # check to see if user has admin permissions
        self.assertNotIn(admin_group, self.instance.groups.all())
        response = self.client.get(self.test_url)
        self.assertIn(admin_group, self.instance.groups.all())

        # check to see if user has adm admin permissions
        self.assertNotIn(adm_admin_group, self.instance.groups.all())
        response = self.client.get(self.test_url1)
        self.assertIn(adm_admin_group, self.instance.groups.all())


class TripRequestDetails(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres
        self.trip_request = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_detail', args=(self.trip_request.pk, ))
        self.expected_template = 'travel/trip_request_detail.html'

    @tag("trip_request", 'detail', "view")
    def test_view_class(self):
        self.assert_inheritance(views.TripRequestDetailView, views.TravelAccessRequiredMixin)
        self.assert_inheritance(views.TripRequestDetailView, CommonDetailView)

    @tag("trip_request", 'detail')
    def test_access(self):
        # only logged in users can access the landing
        super().assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    @tag("trip_request", 'detail', "field_list")
    def test_fields(self):
        fields_to_test = [
            "fiscal_year"
        ]
        self.assert_field_in_field_list(self.test_url, "field_list", fields_to_test)

    # Test that the context contains the proper vars
    @tag("trip_request", 'detail', "context")
    def test_context(self):
        context_vars = [
            "field_list",
            "child_field_list",
            "reviewer_field_list",
            "conf_field_list",
            "cost_field_list",
            "help_text_dict",
            "help_text_dict",
            "fy",
            "is_admin",
            "is_owner",
            "is_current_reviewer",
            "can_modify",
            "trip",
            "triprequest",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

        activate('en')
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        # expected to determine if the user is authorized to add content

        # a random user should not be an admin, owner, current_reviewer, able-to-modify
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], False)
        # self.assertEqual(response.context["report_mode"], True)
        # self.assertIsNone(response.context["can_modify"], False)
        self.assertIsNone(response.context["is_current_reviewer"], True)

        # if owner, the is_owner var should be true
        self.trip_request.user = reg_user
        self.trip_request.save()
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], True)
        self.assertIsNone(response.context["is_current_reviewer"], True)

        # if a user is an admin, they should be able to modify and are also always the current_reviewer
        self.get_and_login_user(in_group='travel_admin')
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], True)
        self.assertEqual(response.context["is_owner"], False)
        self.assertEqual(response.context["is_current_reviewer"], True)

        # if a regular user is the current reviewer
        my_reviewer = FactoryFloor.ReviewerFactory(trip_request=self.trip_request, status=1)
        self.get_and_login_user(user=my_reviewer.user)
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["is_admin"], False)
        self.assertEqual(response.context["is_owner"], False)
        self.assertEqual(response.context["is_current_reviewer"], True)

        # a submitted project being viewed by someone who is not admin or not current reviewer should have report_mode set to True
        self.trip_request.submitted = timezone.now()
        self.trip_request.save()
        reg_user = self.get_and_login_user()
        response = self.client.get(self.test_url)
        self.assertEqual(response.context["report_mode"], True)


class TripRequestListView(CommonTest):
    def setUp(self):
        super().setUp()
        self.tr = FactoryFloor.IndividualTripRequestFactory()
        self.test_url = reverse_lazy('travel:request_list', args=("my",))
        self.expected_template = 'travel/trip_request_list.html'

    @tag("trip_request", 'list', "view")
    def test_view_class(self):
        # make sure the view is inheriting from CanModify Mixin
        self.assert_inheritance(views.TripRequestListView, CommonFilterView)
        self.assert_inheritance(views.TripRequestListView, views.TravelAccessRequiredMixin)

    @tag("trip_request", 'list', "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        # create an admin user (who should always be able to delete) and check to see there is a 200 response
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template)

    # Test that the context contains the proper vars
    @tag("trip_request", 'list', "context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars)

    @tag("trip_request", 'list', "custom")
    def test_excludes_child_requests(self):
        # TODO: make sure that the list is not showing child requests
        pass
