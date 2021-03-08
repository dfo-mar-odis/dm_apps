from django.test import tag
from django.utils import timezone
from django.utils.translation import activate

from shared_models.models import Region
from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory
from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from travel.views import can_modify_request
from .. import utils, models


class UtilsTest(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres

    @tag("utils", )
    def test_in_admin_group(self):
        user = self.get_and_login_user()
        admin = self.get_and_login_user(in_group='travel_admin')
        adm_admin = self.get_and_login_user(in_group='travel_adm_admin')
        self.assertFalse(utils.in_travel_admin_group(user))
        self.assertFalse(utils.in_travel_admin_group(adm_admin))
        self.assertTrue(utils.in_travel_admin_group(admin))

    @tag("utils", )
    def test_in_adm_admin_group(self):
        user = self.get_and_login_user()
        admin = self.get_and_login_user(in_group='travel_admin')
        adm_admin = self.get_and_login_user(in_group='travel_adm_admin')
        self.assertFalse(utils.in_adm_admin_group(user))
        self.assertFalse(utils.in_adm_admin_group(admin))
        self.assertTrue(utils.in_adm_admin_group(adm_admin))

    @tag("utils", )
    def test_as_admin(self):
        user = self.get_and_login_user()
        admin = self.get_and_login_user(in_group='travel_admin')
        adm_admin = self.get_and_login_user(in_group='travel_adm_admin')
        self.assertFalse(utils.is_admin(user))
        self.assertTrue(utils.is_admin(admin))
        self.assertTrue(utils.is_admin(adm_admin))

    @tag("utils", )
    def test_is_approver(self):
        user = self.get_and_login_user()
        trip_request = FactoryFloor.TripRequestFactory(status=17)
        self.assertFalse(utils.is_approver(user, trip_request))
        FactoryFloor.ReviewerFactory(user=user, request=trip_request, status=1)
        self.assertTrue(utils.is_approver(user, trip_request))

    @tag("utils", )
    def test_is_trip_approver(self):
        user = self.get_and_login_user()
        trip = FactoryFloor.TripFactory(status=31)
        self.assertFalse(utils.is_trip_approver(user, trip))
        FactoryFloor.TripReviewerFactory(user=user, trip=trip, status=25)
        self.assertTrue(utils.is_trip_approver(user, trip))

    @tag("utils", )
    def test_is_adm(self):
        # scenario #1
        user = self.get_and_login_user()
        self.assertFalse(utils.is_adm(user))
        national_branch, created = Region.objects.get_or_create(name="national")
        national_branch.head = user
        national_branch.save()
        self.assertTrue(utils.is_adm(user))
        # scenario #2
        user = self.get_and_login_user()
        self.assertFalse(utils.is_adm(user))
        models.DefaultReviewer.objects.get_or_create(user=user, special_role=5)
        national_branch.head = user
        national_branch.save()
        self.assertTrue(utils.is_adm(user))

    @tag("utils", )
    def test_get_request_reviewers(self):
        # create your cast of people
        section = SectionFactory(head=UserFactory(), admin=UserFactory())
        division = section.division
        division.head = UserFactory()
        division.save()
        branch = division.branch
        branch.admin = UserFactory()
        branch.head = UserFactory()
        branch.save()
        region = branch.region
        region.head = UserFactory()
        region.save()
        adm, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=5)
        presection2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        presection1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        presection2.sections.add(section)
        presection1.sections.add(section)
        prediv2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        prediv1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        prediv2.divisions.add(division)
        prediv1.divisions.add(division)
        prebranch2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        prebranch1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        prebranch2.branches.add(branch)
        prebranch1.branches.add(branch)

        trip_request = FactoryFloor.TripRequestFactory(status=17, section=section)
        trip = trip_request.trip
        trip.is_adm_approval_required = True
        trip.is_virtual = False
        trip.save()

        self.assertEqual(trip_request.reviewers.count(), 0)
        utils.get_request_reviewers(trip_request)
        supposed_reviewer_list = [
            presection1.user,
            presection2.user,
            section.admin,
            section.head,
            prediv1.user,
            prediv2.user,
            division.head,
            prebranch1.user,
            prebranch2.user,
            branch.admin,
            branch.head,
            adm.user,
            region.head
        ]
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

        # if there is a regional delegate for expenditure initiation, this should take place of RDG
        ## this only applies to domestic travel... so we will have to remove ADM as well
        trip.is_adm_approval_required = False
        trip.save()
        ei, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), expenditure_initiation_region=region)
        trip_request.reviewers.all().delete()
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        supposed_reviewer_list.append(ei.user)
        utils.get_request_reviewers(trip_request)
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

        # if the trip is virtual, there would be no expenditure initiation
        trip.is_virtual = True
        trip.save()
        trip_request.reviewers.all().delete()
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        utils.get_request_reviewers(trip_request)
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

    @tag("utils", )
    def test_start_request_review_process(self):
        # create your cast of people
        trip_request = FactoryFloor.TripRequestFactory(status=8)
        for i in range(0, 5):
            # add a status date just to make sure it is removed
            FactoryFloor.ReviewerFactory(request=trip_request, status=4, status_date=timezone.now())
        for r in trip_request.reviewers.all():
            self.assertEqual(r.status, 4)
            self.assertIsNotNone(r.status_date)
        utils.start_request_review_process(trip_request)
        for r in trip_request.reviewers.all():
            self.assertEqual(r.status, 20)
            self.assertIsNone(r.status_date)

    @tag("utils", )
    def test_end_request_review_process(self):
        trip_request = FactoryFloor.TripRequestFactory(status=8)
        for i in range(0, 5):
            # add a status date just to make sure it is removed
            FactoryFloor.ReviewerFactory(request=trip_request, status=20, status_date=timezone.now(), comments="123")
        for r in trip_request.reviewers.all():
            self.assertEqual(r.status, 20)
            self.assertIsNotNone(r.status_date)
            self.assertIsNotNone(r.comments)
        utils.end_request_review_process(trip_request)
        for r in trip_request.reviewers.all():
            self.assertEqual(r.status, 4)
            self.assertIsNone(r.status_date)
            self.assertIsNone(r.comments)

    @tag("utils", )
    def test_get_trip_reviewers(self):
        # create your cast of people
        section = SectionFactory(head=UserFactory(), admin=UserFactory())
        division = section.division
        division.head = UserFactory()
        division.save()
        branch = division.branch
        branch.admin = UserFactory()
        branch.head = UserFactory()
        branch.save()
        region = branch.region
        region.head = UserFactory()
        region.save()
        adm, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=5)
        presection2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        presection1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        presection2.sections.add(section)
        presection1.sections.add(section)
        prediv2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        prediv1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        prediv2.divisions.add(division)
        prediv1.divisions.add(division)
        prebranch2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=2)
        prebranch1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), order=1)
        prebranch2.branches.add(branch)
        prebranch1.branches.add(branch)

        trip_request = FactoryFloor.TripRequestFactory(status=17, section=section)
        trip = trip_request.trip
        trip.is_adm_approval_required = True
        trip.is_virtual = False
        trip.save()

        self.assertEqual(trip_request.reviewers.count(), 0)
        utils.get_request_reviewers(trip_request)
        supposed_reviewer_list = [
            presection1.user,
            presection2.user,
            section.admin,
            section.head,
            prediv1.user,
            prediv2.user,
            division.head,
            prebranch1.user,
            prebranch2.user,
            branch.admin,
            branch.head,
            adm.user,
            region.head
        ]
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

        # if there is a regional delegate for expenditure initiation, this should take place of RDG
        ## this only applies to domestic travel... so we will have to remove ADM as well
        trip.is_adm_approval_required = False
        trip.save()
        ei, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), expenditure_initiation_region=region)
        trip_request.reviewers.all().delete()
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        supposed_reviewer_list.append(ei.user)
        utils.get_request_reviewers(trip_request)
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

        # if the trip is virtual, there would be no expenditure initiation
        trip.is_virtual = True
        trip.save()
        trip_request.reviewers.all().delete()
        supposed_reviewer_list = supposed_reviewer_list[:-1]
        utils.get_request_reviewers(trip_request)
        actual_reviewer_list = [r.user for r in trip_request.reviewers.all()]
        self.assertEqual(supposed_reviewer_list, actual_reviewer_list)

    @tag("utils", )
    def test_start_trip_review_process(self):
        trip = FactoryFloor.TripFactory(status=41)
        for i in range(0, 5):
            # add a status date just to make sure it is removed
            FactoryFloor.TripReviewerFactory(trip=trip, status=23, status_date=timezone.now(), comments="123")
        for r in trip.reviewers.all():
            self.assertEqual(r.status, 23)
            self.assertIsNotNone(r.status_date)
        utils.start_trip_review_process(trip, False)
        self.assertEqual(trip.status, 31)
        for r in trip.reviewers.all():
            self.assertEqual(r.status, 24)
            self.assertIsNone(r.status_date)

        # do it again but with rest=True
        trip = FactoryFloor.TripFactory(status=41)
        for i in range(0, 5):
            # add a status date just to make sure it is removed
            FactoryFloor.TripReviewerFactory(trip=trip, status=23, status_date=timezone.now(), comments="123")
        for r in trip.reviewers.all():
            self.assertEqual(r.status, 23)
            self.assertIsNotNone(r.status_date)
        utils.start_trip_review_process(trip, True)
        self.assertEqual(trip.status, 41)
        for r in trip.reviewers.all():
            self.assertEqual(r.status, 24)
            self.assertIsNotNone(r.status_date)

    @tag("utils", 'can_modify')
    def test_can_modify_rules(self):
        activate('en')

        # actors
        trip_request = FactoryFloor.TripRequestFactory()
        traveller = FactoryFloor.TravellerFactory(request=trip_request)
        reg_user = self.get_and_login_user()
        admin_user = self.get_and_login_user(in_group="travel_admin")
        adm_admin_user = self.get_and_login_user(in_group="travel_adm_admin")

        # RULE 1: travel admin = True
        self.assertEqual(can_modify_request(admin_user, trip_request.id), True)
        self.assertEqual(can_modify_request(adm_admin_user, trip_request.id), True)

        # RULE 2: a current reviewer; they must be able to edit a child trip and the parent trip
        # a)
        my_reviewer = FactoryFloor.ReviewerFactory(request=trip_request, status=1)
        trip_request.status = 17
        trip_request.save()
        self.assertTrue(can_modify_request(my_reviewer.user, trip_request.id))

        # RULE 3: when a trip is unsubmitted, randos cannot edit
        self.assertFalse(can_modify_request(reg_user, trip_request.id))

        # RULE 4: when a trip is unsubmitted, owners can edit
        self.assertTrue(can_modify_request(trip_request.created_by, trip_request.id))

        # RULE 5: when a trip is unsubmitted, travellers can edit
        self.assertTrue(can_modify_request(traveller.user, trip_request.id))

        # RULE 6: owners are always able to unsubmit a trip
        trip_request.submitted = timezone.now()
        trip_request.save()
        self.assertTrue(can_modify_request(trip_request.created_by, trip_request.id, True))
        trip_request.status = 22
        trip_request.save()
        self.assertTrue(can_modify_request(trip_request.created_by, trip_request.id, True))

    # @tag("utils", 'get_related_trips')
    # def test_get_related_trips(self):
    #     activate('en')
    #
    #     # actors
    #     ind_request = FactoryFloor.IndividualTripRequestFactory()
    #     child_request = FactoryFloor.ChildTripRequestFactory()
    #     child_request1 = FactoryFloor.ChildTripRequestFactory()
    #     parent_request = child_request.parent_request
    #     random_request = FactoryFloor.IndividualTripRequestFactory()
    #
    #     reg_user = self.get_and_login_user()
    #
    #     # to start, this user should have 0 trips
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 0)
    #
    #     # setting the individual request to user should result in 1 trip
    #     ind_request.user = reg_user
    #     ind_request.save()
    #     self.assertIn(ind_request, utils.get_related_trips(reg_user))
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 1)
    #
    #     # setting parent of group trip to user should increase by 1...
    #     parent_request.user = reg_user
    #     parent_request.save()
    #     self.assertIn(parent_request, utils.get_related_trips(reg_user))
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 2)
    #
    #     # setting parent of child trip to user should NOT increase by 1, since this is the same trip as the parent trip...
    #     child_request.user = reg_user
    #     child_request.save()
    #     self.assertNotIn(child_request, utils.get_related_trips(reg_user))
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 2)
    #
    #     # setting parent of child trip to user should increase by 1...
    #     child_request1.user = reg_user
    #     child_request1.save()
    #     self.assertIn(child_request1.parent_request, utils.get_related_trips(reg_user))
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 3)
    #
    #     # setting created_by of random trip to user should increase by 1...
    #     random_request.created_by = reg_user
    #     random_request.save()
    #     self.assertIn(random_request, utils.get_related_trips(reg_user))
    #     self.assertEqual(utils.get_related_trips(reg_user).count(), 4)
    #
    # @tag("utils", 'trip_review_process')
    # def test_trip_review_process(self):
    #     activate('en')
    #
    #     # actors
    #     trip = FactoryFloor.TripFactory(status=41)  # unreviewed, verified
    #     reviewer1 = FactoryFloor.TripReviewerFactory(trip=trip, order=1)
    #     reviewer2 = FactoryFloor.TripReviewerFactory(trip=trip, order=2)
    #     reviewer3 = FactoryFloor.TripReviewerFactory(trip=trip, order=3)
    #
    #     self.assertIsNone(trip.review_start_date)
    #     utils.start_trip_review_process(trip)
    #     self.assertEqual(trip.status, 31)
    #     self.assertIsNotNone(trip.review_start_date)
    #     for reviewer in trip.reviewers.all():
    #         self.assertEqual(reviewer.status, 24)
    #         self.assertIsNone(reviewer.status_date)
    #
    #     # now let's end the review process
    #     utils.end_trip_review_process(trip)
    #     self.assertEqual(trip.status, 41)
    #     # the timestamp should not be undone
    #     self.assertIsNotNone(trip.review_start_date)
    #     for reviewer in trip.reviewers.all():
    #         self.assertEqual(reviewer.status, 23)
    #         self.assertIsNone(reviewer.status_date)
    #
    # @tag("utils", 'tr_review_process')
    # def test_tr_review_process(self):
    #     activate('en')
    #
    #     # actors
    #     tr = FactoryFloor.IndividualTripRequestFactory(status=8)  # draft
    #     reviewer1 = FactoryFloor.ReviewerFactory(trip_request=tr, order=1)
    #     reviewer2 = FactoryFloor.ReviewerFactory(trip_request=tr, order=2)
    #     reviewer3 = FactoryFloor.ReviewerFactory(trip_request=tr, order=3)
    #
    #     utils.start_request_review_process(tr)
    #     for reviewer in tr.reviewers.all():
    #         self.assertEqual(reviewer.status, 20)
    #         self.assertIsNone(reviewer.status_date)
    #
    #     # now let's end the review process
    #     utils.end_request_review_process(tr)
    #     for reviewer in tr.reviewers.all():
    #         self.assertEqual(reviewer.status, 4)
    #         self.assertIsNone(reviewer.status_date)

# TODO: trip approval seeker
# TODO: trip request approval seeker
