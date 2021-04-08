from django.test import tag
from django.urls import reverse
from django.utils import timezone
from faker import Factory
from rest_framework import status

from . import FactoryFloor
from .. import models
from ..test.common_tests import CommonProjectTest as CommonTest

faker = Factory.create()


class TestActivityListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.obj = FactoryFloor.ActivityFactory(project_year=self.instance)
        self.test_url = reverse("projects2-activity-list", args=[self.instance.pk])

    @tag("api", 'activity-list')
    def test_url(self):
        self.assert_correct_url("projects2-activity-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/activities/")

    @tag("api", 'activity-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'activity-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.ActivityFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.ActivityFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.ActivityFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.ActivityFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.ActivityFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'activity-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestCapitalCostListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.cost = FactoryFloor.CapitalCostFactory(project_year=self.instance)
        self.test_url = reverse("projects2-capital-list", args=[self.instance.pk])

    @tag("api", 'capital-cost')
    def test_url(self):
        self.assert_correct_url("projects2-capital-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/capital-costs/")

    @tag("api", 'capital-cost')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'capital-cost')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.CapitalCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.CapitalCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.CapitalCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.CapitalCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.CapitalCostFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'capital-cost')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestCollaborationListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.obj = FactoryFloor.CollaborationFactory(project_year=self.instance)
        self.test_url = reverse("projects2-collaboration-list", args=[self.instance.pk])

    @tag("api", 'collaboration-list')
    def test_url(self):
        self.assert_correct_url("projects2-collaboration-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/collaborations/")

    @tag("api", 'collaboration-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'collaboration-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.CollaborationFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.CollaborationFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        data = FactoryFloor.CollaborationFactory.get_valid_data()
        response = self.client.post(self.test_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.CollaborationFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.CollaborationFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'collaboration-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestCurrentUser(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.test_url = reverse("projects2-current-user")

    @tag("api", 'current-project-user')
    def test_url(self):
        self.assert_correct_url("projects2-current-user", expected_url_path=f"/api/project-planning/user/")

    @tag("api", 'current-project-user')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'current-project-user')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'current-project-user')
    def test_response_data(self):
        data = self.client.get(self.test_url).data
        keys = ["id", "first_name", "last_name", "username", "is_admin", "is_management", "is_rds"]
        self.assert_dict_has_keys(data, keys)

        # check query params
        object = FactoryFloor.ProjectFactory()
        data = self.client.get(self.test_url + f"?project={object.id}").data
        keys.extend(["reason", "can_modify"])
        self.assert_dict_has_keys(data, keys)

        object = FactoryFloor.StatusReportFactory()
        data = self.client.get(self.test_url + f"?status_report={object.id}").data
        keys.extend(["is_section_head"])
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'current-project-user')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestFileListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.obj = FactoryFloor.FileFactory(project_year=self.instance)
        self.test_url = reverse("projects2-file-list", args=[self.instance.pk])

    @tag("api", 'file-list')
    def test_url(self):
        self.assert_correct_url("projects2-file-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/files/")

    @tag("api", 'file-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'file-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.FileFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.FileFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.FileFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.FileFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.FileFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'file-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


# class TestReviewListCreateAPIView(CommonTest):
#     def setUp(self):
#         super().setUp()
#         self.user = self.get_and_login_user()
#         self.staff = FactoryFloor.LeadStaffFactory()
#         self.instance = self.staff.project_year
#         self.obj = FactoryFloor.ReviewFactory(project_year=self.instance)
#         self.test_url = reverse("projects2-review-list", args=[self.instance.pk])
#
#     @tag("api", 'review-list')
#     def test_url(self):
#         self.assert_correct_url("projects2-review-list", test_url_args=[self.instance.pk],
#                                 expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/reviews/")
#
#     @tag("api", 'review-list')
#     def test_get(self):
#         # PERMISSIONS
#         # authenticated users
#         response = self.client.get(self.test_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # unauthenticated users
#         self.client.logout()
#         response = self.client.get(self.test_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # RESPONSE DATA
#         valid_user = None
#         self.get_and_login_user(user=None)
#         response = self.client.get(self.test_url)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["id"], self.instance.id)
#
#     @tag("api", 'review-list')
#     def test_post(self):
#         # PERMISSIONS
#         # authenticated users
#         response = self.client.post(self.test_url, data=FactoryFloor.ReviewFactory.get_valid_data())
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         # unauthenticated users
#         self.client.logout()
#         response = self.client.post(self.test_url, data=FactoryFloor.ReviewFactory.get_valid_data())
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         # lead staff user
#         self.get_and_login_user(user=self.staff.user)
#         response = self.client.post(self.test_url, data=FactoryFloor.ReviewFactory.get_valid_data())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # RESPONSE DATA
#         valid_user = self.staff.user
#         self.get_and_login_user(user=self.staff.user)
#         response = self.client.post(self.test_url, data=FactoryFloor.ReviewFactory.get_valid_data())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         data = self.client.post(self.test_url, data=FactoryFloor.ReviewFactory.get_valid_data()).data
#         keys = [
#             "id",
#         ]
#         self.assert_dict_has_keys(data, keys)
#
#     @tag("api", 'review-list')
#     def test_unallowed_methods_only(self):
#         restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
#         self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
#         self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
#         self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)
class TestFTEBreakdownAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.test_url = reverse("projects2-fte-breakdown", args=None)

    @tag("api", 'fte-breakdown')
    def test_url(self):
        self.assert_correct_url("projects2-fte-breakdown", test_url_args=None, expected_url_path=f"/api/project-planning/fte-breakdown/")

    @tag("api", 'fte-breakdown')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'fte-breakdown')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'fte-breakdown')
    def test_response_data(self):
        staff1 = FactoryFloor.StaffFactory(user=self.user)
        staff2 = FactoryFloor.StaffFactory(user=self.user)

        data = self.client.get(self.test_url).data

        # Since there was no fiscal year specified, it will be a list of dicts
        keys = [
            'name',
            'fiscal_year',
            'draft',
            'submitted_unapproved',
            'approved',
        ]
        for item in data:
            self.assert_dict_has_keys(item, keys)

        # if we specify a fiscal year, it should just be one obj
        data = self.client.get(self.test_url + f"?year={staff1.project_year.fiscal_year_id}").data
        self.assert_dict_has_keys(data, keys)
        self.assertEqual(data["name"], f"{self.user.last_name}, {self.user.first_name}")

        # we have the option to specify a user
        staff3 = FactoryFloor.StaffFactory(user=self.get_and_login_user())
        data = self.client.get(self.test_url + f"?year={staff3.project_year.fiscal_year_id}").data
        self.assertEqual(data["name"], f"{staff3.user.last_name}, {staff3.user.first_name}")

        # and finally, we should be able to supply a list of project_year ids
        project_year_1 = FactoryFloor.ProjectYearFactory(start_date=timezone.now())
        project_year_2 = FactoryFloor.ProjectYearFactory(start_date=timezone.now())
        staff3 = FactoryFloor.StaffFactory(project_year=project_year_1)
        staff4 = FactoryFloor.StaffFactory(project_year=project_year_2)
        response = self.client.get(self.test_url + f"?ids={project_year_1.id},{project_year_2.id}")
        # but this should return a bad response since no fiscal year was supplied
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.test_url + f"?ids={project_year_1.id},{project_year_2.id};year={project_year_2.fiscal_year_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # the data should be a list for each user
        data = response.data
        self.assertEqual(len(data), 2)
        keys.append("staff_instances")
        for item in data:
            self.assert_dict_has_keys(item, keys)

    @tag("api", 'fte-breakdown')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestOMCostListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.om_cost = FactoryFloor.OMCostFactory(project_year=self.instance)
        self.test_url = reverse("projects2-om-list", args=[self.instance.pk])

    @tag("api", 'om-list')
    def test_url(self):
        self.assert_correct_url("projects2-om-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/om-costs/")

    @tag("api", 'om-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'om-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.OMCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.OMCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=valid_user)
        response = self.client.post(self.test_url, data=FactoryFloor.OMCostFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.OMCostFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'om-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectListAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.instance = FactoryFloor.ProjectFactory()
        self.test_url = reverse("projects2-project-list", args=None)

    @tag("api", 'project-list')
    def test_url(self):
        self.assert_correct_url("projects2-project-list", test_url_args=None, expected_url_path=f"/api/project-planning/projects/")

    @tag("api", 'project-list')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'project-list')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'project-list')
    def test_response_data(self):
        data = self.client.get(self.test_url).data
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], self.instance.id)

    @tag("api", 'project-list')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectRetrieveAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.instance = FactoryFloor.ProjectFactory()
        self.test_url = reverse("projects2-project-detail", args=[self.instance.pk])

    @tag("api", 'project-detail')
    def test_url(self):
        self.assert_correct_url("projects2-project-detail", test_url_args=[self.instance.pk], expected_url_path=f"/api/project-planning/projects/{self.instance.pk}/")

    @tag("api", 'project-detail')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'project-detail')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'project-detail')
    def test_response_data(self):
        data = None
        data = self.client.get(self.test_url, data=data).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'project-detail')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectYearListAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.instance = FactoryFloor.ProjectYearFactory()
        self.test_url = reverse("projects2-year-list", args=None)

    @tag("api", 'year-list')
    def test_url(self):
        self.assert_correct_url("projects2-year-list", test_url_args=None, expected_url_path=f"/api/project-planning/project-years/")

    @tag("api", 'year-list')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'year-list')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'year-list')
    def test_response_data(self):
        self.instance.status = 1
        self.instance.save()
        py = FactoryFloor.ProjectYearFactory(status=4, submitted=timezone.now())
        data = self.client.get(self.test_url).data
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], py.id)
        # but if we are an admin user, we should see 2 projects
        self.get_and_login_user(in_group="projects_admin")
        data = self.client.get(self.test_url).data
        self.assertEqual(len(data["results"]), 2)

    @tag("api", 'year-list')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectYearRetrieveAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.instance = FactoryFloor.ProjectYearFactory()
        self.test_url = reverse("projects2-year-detail", args=[self.instance.pk])

    @tag("api", 'year-detail')
    def test_url(self):
        self.assert_correct_url("projects2-year-detail", test_url_args=[self.instance.pk], expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/")

    @tag("api", 'year-detail')
    def test_authenticated(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'year-detail')
    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("api", 'year-detail')
    def test_response_data(self):
        data = None
        data = self.client.get(self.test_url, data=data).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'year-detail')
    def test_safe_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.post(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectYearSubmitAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.instance.status = 1
        self.instance.save()

        self.test_url = reverse("projects2-year-submit", args=[self.instance.pk])

    @tag("api", 'year-submit')
    def test_url(self):
        self.assert_correct_url("projects2-year-submit", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/submit/")

    @tag("api", 'year-submit')
    def test_permissions(self):
        # authenticated users
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # project lead should be allowed - but will not test extensively the CanModify permissions class since this is done in utils
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'year-submit')
    def test_response_data(self):
        # ensure project is unsubmitted
        self.assertIsNone(self.instance.submitted)

        self.get_and_login_user(user=self.staff.user)
        data = None
        data = self.client.post(self.test_url, data=data).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

        # ensure project is submitted
        self.instance = models.ProjectYear.objects.get(pk=self.instance.id)
        self.assertIsNotNone(self.instance.submitted)
        self.assertEqual(self.instance.submitted.year, timezone.now().year)
        self.assertEqual(self.instance.submitted.month, timezone.now().month)
        self.assertEqual(self.instance.submitted.day, timezone.now().day)
        self.assertEqual(self.instance.status, 2)

    @tag("api", 'year-submit')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.get(self.test_url, data=None).status_code, restricted_statuses)


class TestProjectYearUnsubmitAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.instance.status = 1
        self.instance.save()
        self.instance.submit()
        self.test_url = reverse("projects2-year-unsubmit", args=[self.instance.pk])

    @tag("api", 'year-unsubmit')
    def test_url(self):
        self.assert_correct_url("projects2-year-unsubmit", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/unsubmit/")

    @tag("api", 'year-unsubmit')
    def test_permissions(self):
        # authenticated users
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # project lead should be allowed - but will not test extensively the CanModify permissions class since this is done in utils
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("api", 'year-unsubmit')
    def test_response_data(self):
        # ensure project is submitted
        self.assertIsNotNone(self.instance.submitted)

        self.get_and_login_user(user=self.staff.user)
        data = None
        data = self.client.post(self.test_url, data=data).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

        # ensure project is unsubmitted
        self.instance = models.ProjectYear.objects.get(pk=self.instance.id)
        self.assertIsNone(self.instance.submitted)
        self.assertEqual(self.instance.status, 1)

    @tag("api", 'year-unsubmit')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.get(self.test_url, data=None).status_code, restricted_statuses)


class TestStaffListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.test_url = reverse("projects2-staff-list", args=[self.instance.pk])

    @tag("api", 'staff-list')
    def test_url(self):
        self.assert_correct_url("projects2-staff-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/staff/")

    @tag("api", 'staff-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=valid_user)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'staff-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.StaffFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.StaffFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.StaffFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=valid_user)
        response = self.client.post(self.test_url, data=FactoryFloor.StaffFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    @tag("api", 'staff-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)


class TestStatusReportListCreateAPIView(CommonTest):
    def setUp(self):
        super().setUp()
        self.user = self.get_and_login_user()
        self.staff = FactoryFloor.LeadStaffFactory()
        self.instance = self.staff.project_year
        self.obj = FactoryFloor.StatusReportFactory(project_year=self.instance)
        self.test_url = reverse("projects2-status-report-list", args=[self.instance.pk])

    @tag("api", 'status-report-list')
    def test_url(self):
        self.assert_correct_url("projects2-status-report-list", test_url_args=[self.instance.pk],
                                expected_url_path=f"/api/project-planning/project-years/{self.instance.pk}/status-reports/")

    @tag("api", 'status-report-list')
    def test_get(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unauthenticated users
        self.client.logout()
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # RESPONSE DATA
        valid_user = None
        self.get_and_login_user(user=None)
        response = self.client.get(self.test_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.instance.id)

    @tag("api", 'status-report-list')
    def test_post(self):
        # PERMISSIONS
        # authenticated users
        response = self.client.post(self.test_url, data=FactoryFloor.StatusReportFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # unauthenticated users
        self.client.logout()
        response = self.client.post(self.test_url, data=FactoryFloor.StatusReportFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # lead staff user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.StatusReportFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # RESPONSE DATA
        valid_user = self.staff.user
        self.get_and_login_user(user=self.staff.user)
        response = self.client.post(self.test_url, data=FactoryFloor.StatusReportFactory.get_valid_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.client.post(self.test_url, data=FactoryFloor.StatusReportFactory.get_valid_data()).data
        keys = [
            "id",
        ]
        self.assert_dict_has_keys(data, keys)

    @tag("api", 'status-report-list')
    def test_unallowed_methods_only(self):
        restricted_statuses = [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_403_FORBIDDEN]
        self.assertIn(self.client.put(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.delete(self.test_url, data=None).status_code, restricted_statuses)
        self.assertIn(self.client.patch(self.test_url, data=None).status_code, restricted_statuses)
