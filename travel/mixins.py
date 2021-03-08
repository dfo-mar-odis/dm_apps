from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from travel import models
from travel.utils import in_travel_admin_group, in_adm_admin_group, can_modify_request, is_approver, is_admin


class TravelAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class TravelADMAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_adm_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class CanModifyMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return can_modify_request(self.request.user, self.kwargs.get("pk"))

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class AdminOrApproverRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        my_trip_request = models.TripRequest.objects.get(pk=self.kwargs.get("pk"))
        my_user = self.request.user
        if in_travel_admin_group(my_user) or is_approver(my_user, my_trip_request):
            return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


# This allows any logged in user to access the view
class TravelAccessRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/'
