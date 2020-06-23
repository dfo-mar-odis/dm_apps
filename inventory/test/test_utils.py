from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from shared_models.test.SharedModelsFactoryFloor import UserFactory
from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest
#
#
# class UtilsTest(CommonTravelTest):
#
#     def setUp(self):
#         super().setUp()  # used to import fixutres
#
#     @tag("utils", 'can_modify')
#     def test_can_modify_rules(self):
#         activate('en')
#
#         # actors
#         trip_request = FactoryFloor.IndividualTripRequestFactory()
#         reg_user = self.get_and_login_user()
#         admin_user = self.get_and_login_user(in_group="travel_admin")
#
#         # RULE 1: travel admin = True
#         self.assertEqual(can_modify_request(admin_user, trip_request.id), True)
#
#         # RULE 2: a current reviewer; they must be able to edit a child trip and the parent trip
#         # a)
#         my_reviewer = FactoryFloor.ReviewerFactory(trip_request=trip_request, status_id=1)
#         self.assertEqual(can_modify_request(my_reviewer.user, trip_request.id), True)
#         # b)
#         child_trip_request = FactoryFloor.ChildTripRequestFactory()
#         parent_trip_request = child_trip_request.parent_request
#         my_reviewer = FactoryFloor.ReviewerFactory(trip_request=parent_trip_request, status_id=1)
#         self.assertEqual(can_modify_request(my_reviewer.user, child_trip_request.id), True)
#         self.assertEqual(can_modify_request(my_reviewer.user, parent_trip_request.id), True)
#
#         # RULE 3: when a trip is unsubmitted, randos cannot edit
#         self.assertIsNone(can_modify_request(reg_user, trip_request.id), False)
#         # ** THERE IS AN EXCEPTION HERE: if the trip request user is None, then anyone can edit
#         trip_request.user = None
#         trip_request.save()
#         self.assertEqual(can_modify_request(reg_user, trip_request.id), True)
#         trip_request.user = UserFactory()
#         trip_request.save()
#
#         # RULE 4: when a trip is unsubmitted, owners can edit
#         self.assertEqual(can_modify_request(trip_request.user, trip_request.id), True)
#         self.assertEqual(can_modify_request(parent_trip_request.user, parent_trip_request.id), True)
#         self.assertEqual(can_modify_request(parent_trip_request.user, child_trip_request.id), True)
#
#         # RULE 5: when a trip is unsubmitted, travellers can edit
#         self.assertEqual(can_modify_request(child_trip_request.user, child_trip_request.id), True)
#         self.assertEqual(can_modify_request(child_trip_request.user, parent_trip_request.id), True)
#
#         # RULE 6: owners are always able to unsubmit a trip
#         trip_request.submitted = timezone.now()
#         trip_request.save()
#         self.assertEqual(can_modify_request(trip_request.user, trip_request.id, True), True)
#
#     #
#     # @tag("utils", 'cost_warning')
#     # def test_trip_cost_warning(self):
#     #     activate('en')
#     #
#     #     # actors
#     #     trip_request = FactoryFloor.IndividualTripRequestFactory()
#     #     reg_user = self.get_and_login_user()
#     #     admin_user = self.get_and_login_user(in_group="travel_admin")
#     #
#     #     # scenario 1: trip cost goes over 10K
#
#
# #         """
# #
# # def manage_trip_warning(trip):
# #     This function will decide if sending an email to NCR is necessary based on
# #     1) the total costs accrued for a trip
# #     2) whether or not a warning has already been sent
# #
# #     :param trip: an instance of Trip
# #     :return: NoneObject
# #
# #     # first make sure we are not receiving a NoneObject
# #     try:
# #         trip.non_res_total_cost
# #     except AttributeError:
# #         pass
# #     else:
# #
# #         # If the trip cost is below 10k, make sure the warning field is null and an then do nothing more :)
# #         if trip.non_res_total_cost < 10000:
# #             if trip.cost_warning_sent:
# #                 trip.cost_warning_sent = None
# #                 trip.save()
# #
# #         # if the trip is >= 10K, we simply need to send an email to NCR
# #         else:
# #             if not trip.cost_warning_sent:
# #                 email = emails.TripCostWarningEmail(trip)
# #                 # # send the email object
# #                 custom_send_mail(
# #                     subject=email.subject,
# #                     html_message=email.message,
# #                     from_email=email.from_email,
# #                     recipient_list=email.to_list
# #                 )
# #                 trip.cost_warning_sent = timezone.now()
# #                 trip.save()
# #         """