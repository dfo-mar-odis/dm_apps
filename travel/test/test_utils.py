from django.test import tag
from django.utils import timezone
from django.utils.translation import activate

from shared_models.models import Region
from shared_models.test.SharedModelsFactoryFloor import SectionFactory, UserFactory, DivisionFactory, BranchFactory
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
        ncr_coord2, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=3, order=2)
        ncr_coord1, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=3, order=1)
        adm_recommender, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=4)
        adm, created = models.DefaultReviewer.objects.get_or_create(user=UserFactory(), special_role=5)
        trip = FactoryFloor.TripFactory(status=41, is_adm_approval_required=True)
        self.assertEqual(trip.reviewers.count(), 0)
        utils.get_trip_reviewers(trip)
        supposed_reviewer_list = [
            ncr_coord1.user,
            ncr_coord2.user,
            adm_recommender.user,
            adm.user,
        ]
        actual_reviewer_list = [r.user for r in trip.reviewers.all()]
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

    @tag("utils")
    def test_get_related_requests(self):
        user = UserFactory()
        # scenario 1 --> they are a creator
        trip_request1 = FactoryFloor.TripRequestFactory(created_by=user)
        self.assertIn(trip_request1, utils.get_related_requests(user))
        # scenario 2 --> they are a traveller
        trip_request2 = FactoryFloor.TripRequestFactory(created_by=UserFactory())
        FactoryFloor.TravellerFactory(request=trip_request2, user=user)
        self.assertIn(trip_request2, utils.get_related_requests(user))

    @tag("utils")
    def test_get_related_request_reviewers(self):
        # scenario 1 --> they are the active reviewer
        user = UserFactory()
        trip_request = FactoryFloor.TripRequestFactory(created_by=user, status=17)
        reviewer = FactoryFloor.ReviewerFactory(user=user, request=trip_request, status=4)  # start in draft
        self.assertIsNone(trip_request.current_reviewer)
        reviewer.status = 1
        reviewer.save()
        self.assertEqual(trip_request.current_reviewer, reviewer)
        self.assertIn(reviewer, utils.get_related_request_reviewers(user))
        trip_request.status = 16
        trip_request.save()
        self.assertNotIn(reviewer, utils.get_related_request_reviewers(user))
        trip_request.status = 14
        trip_request.save()
        self.assertNotIn(reviewer, utils.get_related_request_reviewers(user))
        trip_request.status = 8
        trip_request.save()
        self.assertNotIn(reviewer, utils.get_related_request_reviewers(user))

    @tag("utils")
    def test_get_related_trip_reviewers(self):
        # scenario 1 --> they are the active reviewer
        user = UserFactory()
        reviewer = FactoryFloor.TripReviewerFactory(user=user, status=23)  # start in draft
        self.assertIsNone(reviewer.trip.current_reviewer)
        reviewer.status = 25
        reviewer.save()
        self.assertEqual(reviewer.trip.current_reviewer, reviewer)
        self.assertIn(reviewer, utils.get_related_trip_reviewers(user))

    @tag("utils")
    def test_get_adm_eligible_trips(self):
        trip = FactoryFloor.TripFactory(is_adm_approval_required=False, start_date=timezone.now(), trip_subcategory_id=8)
        self.assertNotIn(trip, utils.get_adm_eligible_trips())
        trip.is_adm_approval_required = True
        trip.save()
        self.assertNotIn(trip, utils.get_adm_eligible_trips())
        trip.status = 41
        trip.save()
        self.assertNotIn(trip, utils.get_adm_eligible_trips())
        trip_request = FactoryFloor.TripRequestFactory(trip=trip)
        FactoryFloor.TravellerFactory(request=trip_request)
        self.assertNotIn(trip, utils.get_adm_eligible_trips())
        trip_request.status = 12
        trip_request.save()
        self.assertIn(trip, utils.get_adm_eligible_trips())

    @tag("utils")
    def test_is_manager_or_assistant_or_admin(self):
        section = SectionFactory(head=UserFactory(), admin=UserFactory())
        division = section.division
        division.head = UserFactory()
        division.admin = UserFactory()
        division.save()
        branch = division.branch
        branch.admin = UserFactory()
        branch.head = UserFactory()
        branch.save()
        region = branch.region
        region.head = UserFactory()
        region.admin = UserFactory()
        region.save()
        rando = UserFactory()
        self.assertFalse(utils.is_manager_or_assistant_or_admin(rando))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(section.head))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(division.head))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(branch.head))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(region.head))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(section.admin))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(division.admin))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(branch.admin))
        self.assertTrue(utils.is_manager_or_assistant_or_admin(region.admin))


    @tag("utils")
    def test_get_requests_with_managerial_access(self):
        section1 = SectionFactory(head=UserFactory(), admin=UserFactory())
        division = section1.division
        division.head = UserFactory()
        division.admin = UserFactory()
        division.save()
        branch = division.branch
        branch.admin = UserFactory()
        branch.head = UserFactory()
        branch.save()
        region = branch.region
        region.head = UserFactory()
        region.admin = UserFactory()
        region.save()
        # another section within division
        section2 = SectionFactory(head=UserFactory(), admin=UserFactory(), division=division)
        # another section within branch
        d = DivisionFactory(head=UserFactory(), admin=UserFactory(), branch=branch)
        section3 = SectionFactory(head=UserFactory(), admin=UserFactory(), division=d)
        # another section within region
        b = BranchFactory(head=UserFactory(), admin=UserFactory(), region=region)
        d = DivisionFactory(head=UserFactory(), admin=UserFactory(), branch=b)
        section4 = SectionFactory(head=UserFactory(), admin=UserFactory(), division=d)

        # create 4 trip requests, one under each section
        r1 = FactoryFloor.TripRequestFactory(section=section1)
        r2 = FactoryFloor.TripRequestFactory(section=section2)
        r3 = FactoryFloor.TripRequestFactory(section=section3)
        r4 = FactoryFloor.TripRequestFactory(section=section4)

        # start high: region head should see all four requests
        self.assertEqual(utils.get_requests_with_managerial_access(region.head).count(), 4)
        self.assertEqual(utils.get_requests_with_managerial_access(region.admin).count(), 4)
        for r in [r1, r2, r3, r4]:
            self.assertIn(r, utils.get_requests_with_managerial_access(region.head))
            self.assertIn(r, utils.get_requests_with_managerial_access(region.admin))

        # branch head should see all 3 requests
        self.assertEqual(utils.get_requests_with_managerial_access(branch.head).count(), 3)
        self.assertEqual(utils.get_requests_with_managerial_access(branch.admin).count(), 3)
        for r in [r1, r2, r3]:
            self.assertIn(r, utils.get_requests_with_managerial_access(branch.head))
            self.assertIn(r, utils.get_requests_with_managerial_access(branch.admin))

        # division head should see all 2 requests
        self.assertEqual(utils.get_requests_with_managerial_access(division.head).count(), 2)
        self.assertEqual(utils.get_requests_with_managerial_access(division.admin).count(), 2)
        for r in [r1, r2]:
            self.assertIn(r, utils.get_requests_with_managerial_access(division.head))
            self.assertIn(r, utils.get_requests_with_managerial_access(division.admin))

        # section head should see all 1 requests
        self.assertEqual(utils.get_requests_with_managerial_access(section1.head).count(), 1)
        self.assertEqual(utils.get_requests_with_managerial_access(section1.admin).count(), 1)
        for r in [r1]:
            self.assertIn(r, utils.get_requests_with_managerial_access(section1.head))
            self.assertIn(r, utils.get_requests_with_managerial_access(section1.admin))

    @tag("utils")
    def test_cherry_pick_traveller(self):
        """ because of the complications of having a request obj in here, we will test this through the api view tests"""
        pass