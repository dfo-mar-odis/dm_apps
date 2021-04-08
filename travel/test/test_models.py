from django.test import tag
from django.utils.translation import gettext as _
from faker import Faker

from shared_models import models as shared_models
from shared_models.test.SharedModelsFactoryFloor import SectionFactory, RegionFactory, BranchFactory, DivisionFactory
from travel.test.common_tests import CommonTravelTest as CommonTest
from . import FactoryFloor
from .. import models

faker = Faker()


class TestHelpTextModel(CommonTest):
    def setUp(self):
        super().setUp()

    @tag('HelpText', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'field_name',
            'eng_text',
            'fra_text',
        ]
        self.assert_has_fields(models.HelpText, fields_to_check)

    @tag('HelpText', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['field_name', ]
        self.assert_mandatory_fields(models.HelpText, fields_to_check)


class TestDefaultReviewerModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.DefaultReviewerFactory()

    @tag('DefaultReviewer', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'user',
            'expenditure_initiation_region',
            'special_role',
            'order',
        ]
        self.assert_has_fields(models.DefaultReviewer, fields_to_check)

    @tag('DefaultReviewer', 'models', '12m')
    def test_12m_expenditure_initiation_region(self):
        # a `default_reviewer` that is attached to a given `expenditure_initiation_region` should be accessible by the reverse name `default_reviewers`
        expenditure_initiation_region = RegionFactory()
        my_instance = self.instance
        my_instance.expenditure_initiation_region = expenditure_initiation_region
        my_instance.save()
        self.assertIn(my_instance, expenditure_initiation_region.travel_default_reviewers.all())

    @tag('DefaultReviewer', 'models', 'm2m')
    def test_m2m_sections(self):
        # a `default_reviewer` that is attached to a given `sections` should be accessible by the m2m field name `sections`
        section = SectionFactory()
        self.instance.sections.add(section)
        self.assertEqual(self.instance.sections.count(), 1)
        self.assertIn(section, self.instance.sections.all())

    @tag('DefaultReviewer', 'models', 'm2m')
    def test_m2m_divisions(self):
        # a `default_reviewer` that is attached to a given `divisions` should be accessible by the m2m field name `divisions`
        division = DivisionFactory()
        self.instance.divisions.add(division)
        self.assertEqual(self.instance.divisions.count(), 1)
        self.assertIn(division, self.instance.divisions.all())

    @tag('DefaultReviewer', 'models', 'm2m')
    def test_m2m_branches(self):
        # a `default_reviewer` that is attached to a given `branch` should be accessible by the m2m field name `branches`
        branch = BranchFactory()
        self.instance.branches.add(branch)
        self.assertEqual(self.instance.branches.count(), 1)
        self.assertIn(branch, self.instance.branches.all())

    @tag('DefaultReviewer', 'models', 'choices')
    def test_special_role(self):
        actual_choices = (
            (3, _("NCR Travel Coordinators")),
            (4, _("ADM Recommender")),
            (5, _("ADM")),
        )
        expected_choices = [field.choices for field in models.DefaultReviewer._meta.fields if field.name == "special_role"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('DefaultReviewer', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['user', ]
        self.assert_mandatory_fields(models.DefaultReviewer, fields_to_check)


class TestNJCRatesModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = models.NJCRates.objects.all()[faker.random_int(0, models.NJCRates.objects.count() - 1)]

    @tag('NJCRates', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["amount", "last_modified", ]
        self.assert_has_fields(models.NJCRates, fields_to_check)

    @tag('NJCRates', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)

    @tag('NJCRates', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['amount', ]
        self.assert_mandatory_fields(models.NJCRates, fields_to_check)


class TestProcessStepModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ProcessStepFactory()

    @tag('ProcessStep', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'stage',
            'order',
            'is_visible',
        ]
        self.assert_has_fields(models.ProcessStep, fields_to_check)

    @tag('ProcessStep', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.Lookup)

    @tag('ProcessStep', 'models', 'choices')
    def test_choices_stage(self):
        actual_choices = (
            (0, _("Information Section")),
            (1, _("Travel Request Process Outline")),
            (2, _("Review Process Outline")),
        )
        expected_choices = [field.choices for field in models.ProcessStep._meta.fields if field.name == "stage"][0]
        self.assertEqual(actual_choices, expected_choices)


class TestFAQModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FAQFactory()

    @tag('FAQ', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'question_en',
            'question_fr',
            'answer_en',
            'answer_fr',
            'order',
        ]
        self.assert_has_fields(models.FAQ, fields_to_check)

    @tag('FAQ', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.FAQ, ["tquestion", "tanswer"])


class TestReferenceMaterialModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ReferenceMaterialFactory()

    @tag('ReferenceMaterial', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'order',
            'url_en',
            'url_fr',
            'file_en',
            'file_fr',
            'created_at',
            'updated_at',
        ]
        self.assert_has_fields(models.ReferenceMaterial, fields_to_check)

    @tag('ReferenceMaterial', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.ReferenceMaterial, [
            "tfile",
            "turl",
        ])

    @tag('ReferenceMaterial', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)


class TestCostCategoryModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = models.CostCategory.objects.all()[faker.random_int(0, models.CostCategory.objects.count() - 1)]

    @tag('CostCategory', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["order", ]
        self.assert_has_fields(models.CostCategory, fields_to_check)

    @tag('CostCategory', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)


class TestCostModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)]

    @tag('Cost', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["cost_category", ]
        self.assert_has_fields(models.Cost, fields_to_check)

    @tag('Cost', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)

    @tag('Cost', 'models', '12m')
    def test_12m_cost_category(self):
        # a `cost` that is attached to a given `cost_category` should be accessible by the reverse name `costs`
        cost_category = models.CostCategory.objects.all()[faker.random_int(0, models.CostCategory.objects.count() - 1)]
        my_instance = self.instance
        my_instance.cost_category = cost_category
        my_instance.save()
        self.assertIn(my_instance, cost_category.cost_set.all())


class TestRoleModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.RoleFactory()

    @tag('Role', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)


class TestTripCategoryModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = models.TripCategory.objects.all()[faker.random_int(0, models.TripCategory.objects.count() - 1)]

    @tag('TripCategory', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["days_when_eligible_for_review", ]
        self.assert_has_fields(models.TripCategory, fields_to_check)

    @tag('TripCategory', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.SimpleLookup)


class TestTripSubcategoryModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)]

    @tag('TripSubcategory', 'models', 'fields')
    def test_fields(self):
        fields_to_check = ["trip_category", ]
        self.assert_has_fields(models.TripSubcategory, fields_to_check)

    @tag('TripSubcategory', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.TripSubcategory, ["tname"])

    @tag('TripSubcategory', 'models', 'inheritance')
    def test_inheritance(self):
        self.assert_inheritance(type(self.instance), shared_models.Lookup)

    @tag('TripSubcategory', 'models', '12m')
    def test_12m_trip_category(self):
        # a `trip_subcategory` that is attached to a given `trip_category` should be accessible by the reverse name `subcategories`
        trip_category = models.TripCategory.objects.all()[faker.random_int(0, models.TripCategory.objects.count() - 1)]
        my_instance = self.instance
        my_instance.trip_category = trip_category
        my_instance.save()
        self.assertIn(my_instance, trip_category.subcategories.all())


class TestTripModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripFactory()

    @tag('Trip', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'abstract_deadline',
            'adm_review_deadline',
            'admin_notes',
            'cost_warning_sent',
            'created_at',
            'created_by',
            'date_eligible_for_adm_review',
            'end_date',
            'fiscal_year',
            'has_event_template',
            'is_adm_approval_required',
            'is_verified',
            'is_virtual',
            'lead',
            'location',
            'meeting_url',
            'name',
            'nom',
            'notes',
            'number',
            'registration_deadline',
            'review_start_date',
            'start_date',
            'status',
            'trip_subcategory',
            'updated_at',
            'updated_by',
            'verified_by',
        ]
        self.assert_has_fields(models.Trip, fields_to_check)

    @tag('Trip', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Trip, ['metadata',
                                            'closest_date',
                                            'days_until_eligible_for_adm_review',
                                            'days_until_adm_review_deadline',
                                            'admin_notes_html',
                                            'html_block',
                                            'number_of_days',
                                            'dates',
                                            'travellers',
                                            'total_cost',
                                            'total_non_dfo_cost',
                                            'total_dfo_cost',
                                            'non_res_total_cost',
                                            'total_non_dfo_funding_sources',
                                            'tname',
                                            'current_reviewer',
                                            'trip_review_ready',
                                            ])

    @tag('Trip', 'models', '12m')
    def test_12m_trip_subcategory(self):
        # a `trip` that is attached to a given `trip_subcategory` should be accessible by the reverse name `trips`
        # trip_subcategory = FactoryFloor.TripSubcategoryFactory()
        trip_subcategory = models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)]
        my_instance = self.instance
        my_instance.trip_subcategory = trip_subcategory
        my_instance.save()
        self.assertIn(my_instance, trip_subcategory.trips.all())

    @tag('Trip', 'models', '12m')
    def test_12m_trip_subcategory(self):
        # a `trip` that is attached to a given `trip_subcategory` should be accessible by the reverse name `trips`
        # trip_subcategory = FactoryFloor.TripSubcategoryFactory()
        trip_subcategory = models.TripSubcategory.objects.all()[faker.random_int(0, models.TripSubcategory.objects.count() - 1)]
        my_instance = self.instance
        my_instance.trip_subcategory = trip_subcategory
        my_instance.save()
        self.assertIn(my_instance, trip_subcategory.trips.all())

    @tag('Trip', 'models', '12m')
    def test_12m_lead(self):
        # a `trip` that is attached to a given `region` should be accessible by the reverse name `trips`
        region = FactoryFloor.RegionFactory()
        my_instance = self.instance
        my_instance.lead = region
        my_instance.save()
        self.assertIn(my_instance, region.meeting_leads.all())

    @tag('Trip', 'models', 'choices')
    def test_choices_status(self):
        actual_choices = (
            (30, _("Unverified")),
            (31, _("Under review")),
            (32, _("Reviewed")),
            (41, _("Verified")),
            (43, _("Cancelled")),
        )
        expected_choices = [field.choices for field in models.Trip._meta.fields if field.name == "status"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Trip', 'models', 'unique_fields')
    def test_unique_fields(self):
        fields_to_check = ['name', ]
        self.assert_unique_fields(models.Trip, fields_to_check)

    @tag('Trip', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = [
            'name',
            'is_virtual',
            'start_date',
            'end_date',
        ]
        self.assert_mandatory_fields(models.Trip, fields_to_check)


class TestTripRequestModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripRequestFactory()

    @tag('TripRequest', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'uuid',
            'section',
            'trip',
            'objective_of_event',
            'benefit_to_dfo',
            'late_justification',
            'funding_source',
            'notes',
            'admin_notes',
            'submitted',
            'original_submission_date',
            'status',
            'fiscal_year',
            'name_search',
            'creator_search',
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
        ]
        self.assert_has_fields(models.TripRequest, fields_to_check)

    @tag('TripRequest', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.TripRequest, [
            'unsubmit',
            'travellers_from_other_requests',
            'travellers_from_other_regions',
            'region',
            'metadata',
            'admin_notes_html',
            'add_admin_note',
            'request_title',
            'reviewer_order_message',
            'cost_breakdown',
            'total_request_cost',
            'total_non_dfo_funding',
            'total_dfo_funding',
            'total_non_dfo_funding_sources',
            'traveller_count',
            'current_reviewer',
            'adm',
            'expenditure_initiation',
            'recommenders',
            'processing_time',
            'is_late_request',
        ])

    @tag('TripRequest', 'models', '12m')
    def test_12m_trip(self):
        # a `request` that is attached to a given `trip` should be accessible by the reverse name `requests`
        trip = FactoryFloor.TripFactory()
        my_instance = self.instance
        my_instance.trip = trip
        my_instance.save()
        self.assertIn(my_instance, trip.requests.all())

    @tag('TripRequest', 'models', 'm2m')
    def test_m2m_bta_attendee(self):
        # a `request` that is attached to a given `bta_attendee` should be accessible by the m2m field name `bta_attendees`
        bta_attendee = FactoryFloor.UserFactory()
        self.instance.bta_attendees.add(bta_attendee)
        self.assertEqual(self.instance.bta_attendees.count(), 1)
        self.assertIn(bta_attendee, self.instance.bta_attendees.all())

    @tag('TripRequest', 'models', 'choices')
    def test_choices_status(self):
        actual_choices = (
            (8, _("Draft")),
            (17, _("Pending Review")),
            (12, _("Pending Recommendation")),
            (14, _("Pending ADM Approval")),
            (15, _("Pending Expenditure Initiation")),
            (16, _("Changes Requested")),
            (10, _("Denied")),
            (11, _("Approved")),
            (22, _("Cancelled")),
        )
        expected_choices = [field.choices for field in models.TripRequest._meta.fields if field.name == "status"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('TripRequest', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = [
            'trip',
        ]
        self.assert_mandatory_fields(models.TripRequest, fields_to_check)


class TestTravellerModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TravellerFactory()

    @tag('Traveller', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'request',
            'user',
            'is_public_servant',
            'is_research_scientist',
            'first_name',
            'last_name',
            'address',
            'phone',
            'email',
            'company_name',
            'departure_location',
            'start_date',
            'end_date',
            'role',
            'role_of_participant',
            'learning_plan',
            'notes',
            'non_dfo_costs',
            'non_dfo_org',
        ]
        self.assert_has_fields(models.Traveller, fields_to_check)

    @tag('Traveller', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Traveller, [
            'dates',
            'long_role',
            'cost_breakdown',
            'cost_breakdown_html',
            'non_dfo_costs_html',
            'total_cost',
            'total_non_dfo_funding',
            'total_dfo_funding',
            'purpose_long',
            'purpose_long_text',
            'smart_name',
        ])

    @tag('Traveller', 'models', '12m')
    def test_12m_request(self):
        # a `traveller` that is attached to a given `request` should be accessible by the reverse name `travellers`
        request = FactoryFloor.TripRequestFactory()
        my_instance = self.instance
        my_instance.request = request
        my_instance.save()
        self.assertIn(my_instance, request.travellers.all())

    @tag('Traveller', 'models', '12m')
    def test_12m_user(self):
        # a `traveller` that is attached to a given `user` should be accessible by the reverse name `travellers`
        user = FactoryFloor.UserFactory()
        my_instance = self.instance
        my_instance.user = user
        my_instance.save()
        self.assertIn(my_instance, user.travellers.all())

    @tag('Traveller', 'models', 'unique_together')
    def test_unique_together(self):
        expected_unique_together = (('user', 'request'),)
        actual_unique_together = models.Traveller._meta.unique_together
        self.assertEqual(expected_unique_together, actual_unique_together)

    @tag('Traveller', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['request', ]
        self.assert_mandatory_fields(models.Traveller, fields_to_check)


class TestTravellerCostModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TravellerCostFactory()

    @tag('TravellerCost', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'traveller',
            'cost',
            'rate_cad',
            'number_of_days',
            'amount_cad',
        ]
        self.assert_has_fields(models.TravellerCost, fields_to_check)

    @tag('TravellerCost', 'models', '12m')
    def test_12m_traveller(self):
        # a `cost` that is attached to a given `traveller` should be accessible by the reverse name `costs`
        traveller = FactoryFloor.TravellerFactory()
        my_instance = self.instance
        my_instance.traveller = traveller
        my_instance.save()
        self.assertIn(my_instance, traveller.costs.all())

    @tag('TravellerCost', 'models', '12m')
    def test_12m_cost(self):
        # a `cost` that is attached to a given `traveller` should be accessible by the reverse name `costs`
        cost = models.Cost.objects.all()[faker.random_int(0, models.Cost.objects.count() - 1)]
        my_instance = self.instance
        my_instance.cost = cost
        my_instance.save()
        self.assertIn(my_instance, cost.trip_request_costs.all())

    @tag('TravellerCost', 'models', 'unique_together')
    def test_unique_together(self):
        expected_unique_together = (('traveller', 'cost'),)
        actual_unique_together = models.TravellerCost._meta.unique_together
        self.assertEqual(expected_unique_together, actual_unique_together)

    @tag('TravellerCost', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['traveller', 'cost', ]
        self.assert_mandatory_fields(models.TravellerCost, fields_to_check)


class TestReviewerModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ReviewerFactory()

    @tag('Reviewer', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'request',
            'order',
            'user',
            'role',
            'status',
            'status_date',
            'comments',
            'created_at',
            'updated_by',
            'updated_at',
        ]
        self.assert_has_fields(models.Reviewer, fields_to_check)

    @tag('Reviewer', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.Reviewer, [
            "metadata",
            "comments_html",
        ])

    @tag('Reviewer', 'models', '12m')
    def test_12m_request(self):
        # a `reviewer` that is attached to a given `request` should be accessible by the reverse name `reviewers`
        request = FactoryFloor.TripRequestFactory()
        request = models.TripRequest.objects.all()[faker.random_int(0, models.TripRequest.objects.count() - 1)]
        my_instance = self.instance
        my_instance.request = request
        my_instance.save()
        self.assertIn(my_instance, request.reviewers.all())

    @tag('Reviewer', 'models', '12m')
    def test_12m_user(self):
        # a `reviewer` that is attached to a given `user` should be accessible by the reverse name `reviewers`
        user = FactoryFloor.UserFactory()
        my_instance = self.instance
        my_instance.user = user
        my_instance.save()
        self.assertIn(my_instance, user.reviewers.all())

    @tag('Reviewer', 'models', 'choices')
    def test_choices_status(self):
        actual_choices = (
            (4, _("Draft")),
            (20, _("Queued")),
            (1, _("Pending")),
            (2, _("Approved")),
            (3, _("Denied")),
            (5, _("Cancelled")),
            (21, _("Skipped")),
        )
        expected_choices = [field.choices for field in models.Reviewer._meta.fields if field.name == "status"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Reviewer', 'models', 'choices')
    def test_choices_role(self):
        actual_choices = (
            (1, _("Reviewer")),
            (2, _("Recommender")),
            (3, _("NCR Travel Coordinators")),
            (4, _("ADM Recommender")),
            (5, _("ADM")),
            (6, _("Expenditure Initiation")),
            (7, _("RDG (Expenditure Initiation)")),  # this is temporary until RDG is actually looped into the process
        )
        expected_choices = [field.choices for field in models.Reviewer._meta.fields if field.name == "role"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('Reviewer', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = [
            'request',
            'user',
            'role',
            'status',
        ]
        self.assert_mandatory_fields(models.Reviewer, fields_to_check)


class TestTripReviewerModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TripReviewerFactory()

    @tag('TripReviewer', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'trip',
            'order',
            'user',
            'role',
            'status',
            'status_date',
            'comments',
            'created_at',
            'updated_by',
            'updated_at',
        ]
        self.assert_has_fields(models.TripReviewer, fields_to_check)

    @tag('TripReviewer', 'models', 'props')
    def test_props(self):
        self.assert_has_props(models.TripReviewer, ["comments_html", "metadata", ])

    @tag('TripReviewer', 'models', '12m')
    def test_12m_trip(self):
        # a `reviewer` that is attached to a given `trip` should be accessible by the reverse name `reviewers`
        trip = FactoryFloor.TripFactory()
        my_instance = self.instance
        my_instance.trip = trip
        my_instance.save()
        self.assertIn(my_instance, trip.reviewers.all())

    @tag('TripReviewer', 'models', 'unique_together')
    def test_unique_together(self):
        expected_unique_together = (('trip', 'user', 'role',),)
        actual_unique_together = models.TripReviewer._meta.unique_together
        self.assertEqual(expected_unique_together, actual_unique_together)

    @tag('TripReviewer', 'models', 'choices')
    def test_choices_status(self):
        actual_choices = (
            (23, _("Draft")),
            (24, _("Queued")),
            (25, _("Pending")),
            (26, _("Complete")),
            (42, _("Skipped")),
            (44, _("Cancelled")),
        )
        expected_choices = [field.choices for field in models.TripReviewer._meta.fields if field.name == "status"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('TripReviewer', 'models', 'choices')
    def test_choices_role(self):
        actual_choices = (
            (1, _("Reviewer")),
            (2, _("Recommender")),
            (3, _("NCR Travel Coordinators")),
            (4, _("ADM Recommender")),
            (5, _("ADM")),
            (6, _("RDG")),
        )
        expected_choices = [field.choices for field in models.TripReviewer._meta.fields if field.name == "role"][0]
        self.assertEqual(actual_choices, expected_choices)

    @tag('TripReviewer', 'models', 'mandatory_fields')
    def test_mandatory_fields(self):
        fields_to_check = ['trip', 'user', 'role', 'status']
        self.assert_mandatory_fields(models.TripReviewer, fields_to_check)


class TestFileModel(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FileFactory()

    @tag('File', 'models', 'fields')
    def test_fields(self):
        fields_to_check = [
            'request',
            'name',
            'file',
            'date_created',
        ]
        self.assert_has_fields(models.File, fields_to_check)

    @tag('File', 'models', '12m')
    def test_12m_request(self):
        # a `file` that is attached to a given `request` should be accessible by the reverse name `files`
        request = FactoryFloor.TripRequestFactory()
        my_instance = self.instance
        my_instance.request = request
        my_instance.save()
        self.assertIn(my_instance, request.files.all())
