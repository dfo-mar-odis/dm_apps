import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import TextField
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, ListView, TemplateView
###

from lib.functions.custom_functions import nz
from . import models
from . import forms
from . import emails


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'shares/close_me.html'


def in_shares_group(user):
    if user:
        return user.groups.filter(name='shares_access').count() != 0


class SharesAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_shares_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_shares_admin_group(user):
    if user:
        return user.groups.filter(name='shares_admin').count() != 0


class SharesAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_shares_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SharesAdminRequiredMixin, TemplateView):
    template_name = 'shares/index.html'


class EmailListTemplateView(SharesAdminRequiredMixin, TemplateView):
    template_name = 'shares/email_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["user_list"] = models.User.objects.filter(status=2).filter(user__email__isnull=False)
        return context


# SERVER #
##########
class ServerListView(SharesAdminRequiredMixin, ListView):
    model = models.Server

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Server.objects.first()
        context["field_list"] = [
            'server_type',
            'hostname',
            'ip_address',
            'mac_address',
        ]
        return context


class ServerDetailView(SharesAdminRequiredMixin, DetailView):
    model = models.Server

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'server_type',
            'hostname',
            'ip_address',
            'mac_address',
            'notes',
        ]
        return context


class ServerUpdateView(SharesAdminRequiredMixin, UpdateView):
    model = models.Server
    form_class = forms.ServerForm


class ServerCreateView(SharesAdminRequiredMixin, CreateView):
    model = models.Server
    form_class = forms.ServerForm


class ServerCreateViewPopout(SharesAdminRequiredMixin, CreateView):
    model = models.Server
    form_class = forms.ServerForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('shares:close_me'))


class ServerDeleteView(SharesAdminRequiredMixin, DeleteView):
    model = models.Server
    success_url = reverse_lazy('shares:server_list')
    success_message = 'The server was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# USER #
##########
class UserListView(SharesAdminRequiredMixin, ListView):
    model = models.User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.User.objects.first()
        context["field_list"] = [
            'server',
            'username',
            'shares',
            'status',
        ]
        return context


class UserDetailView(SharesAdminRequiredMixin, DetailView):
    model = models.User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'username',
            'password',
            'server',
            'notes',
            'status',
        ]
        return context


class UserUpdateView(SharesAdminRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserForm


class UserCreateView(SharesAdminRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserForm


class UserCreateViewPopout(SharesAdminRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('shares:close_me'))


class UserDeleteView(SharesAdminRequiredMixin, DeleteView):
    model = models.User
    success_url = reverse_lazy('shares:server_list')
    success_message = 'The user was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def send_instructions(request, pk):
    # create a new email object
    my_user = models.User.objects.get(pk=pk)
    email = emails.SendInstructionsEmail(my_user)
    # send the email object
    if settings.USE_EMAIL:
        send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                  recipient_list=email.to_list, fail_silently=False, )
    else:
        print('not sending email since in dev mode')
        print("from={}".format(email.from_email))
        print("to={}".format(email.to_list))
        print("subject={}".format(email.subject))
        print("message={}".format(email.message))

    messages.success(request, "An email has been sent to the user with setup instructions!")

    return HttpResponseRedirect(reverse("shares:user_detail", kwargs={"pk": pk}))


# SHARE #
#########
class ShareListView(SharesAdminRequiredMixin, ListView):
    model = models.Share

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Share.objects.first()
        context["field_list"] = [
            'server',
            'name',
            'local_path',
            'mounted_path',
            'network_path',
        ]
        return context


class ShareDetailView(SharesAdminRequiredMixin, DetailView):
    model = models.Share

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'server',
            'name',
            'local_path',
            'mounted_path',
            'network_path',
            'notes',
        ]
        return context


class ShareUpdateView(SharesAdminRequiredMixin, UpdateView):
    model = models.Share
    form_class = forms.ShareForm


class ShareCreateView(SharesAdminRequiredMixin, CreateView):
    model = models.Share
    form_class = forms.ShareForm


class ShareCreateViewPopout(SharesAdminRequiredMixin, CreateView):
    model = models.Share
    form_class = forms.ShareForm

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse('shares:close_me'))


class ShareDeleteView(SharesAdminRequiredMixin, DeleteView):
    model = models.Share
    success_url = reverse_lazy('shares:server_list')
    success_message = 'The share was deleted successfully!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
