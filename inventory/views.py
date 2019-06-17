import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Value, TextField, Q
from django.db.models.functions import Concat
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
###
from collections import OrderedDict
from . import models
from . import forms
from . import filters
from . import emails
from . import xml_export
from . import reports
from shared_models import models as shared_models


# @login_required(login_url='/accounts/login_required/')
# @user_passes_test(in_herring_group, login_url='/accounts/denied/')

def in_inventory_dm_group(user):
    """returns True if user is in specified group"""
    if user:
        return user.groups.filter(name='inventory_dm').count() > 0


def is_custodian_or_admin(user, resource_id):
    """returns True if user is a custodian in the specified resource"""
    if user.id:
        # first, check to see if user is a dm admin
        if in_inventory_dm_group(user):
            return True
        else:
            # if the user has no associated Person in the app, automatic fail
            try:
                person = models.Person.objects.get(user=user)
            except ObjectDoesNotExist:
                return False
            else:
                # check to see if they are listed as custodian (role_id=1) on the specified resource id
                return models.ResourcePerson.objects.filter(person=person, resource=resource_id, role_id=1).count() > 0


class CustodianRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/custodians-only/')
        return super().dispatch(request, *args, **kwargs)


class InventoryDMRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_inventory_dm_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'inventory/close_me.html'


# RESOURCE #
############

class ResourceListView(FilterView):
    filterset_class = filters.ResourceFilter
    login_url = '/accounts/login_required/'
    template_name = 'inventory/resource_list.html'
    # queryset = models.Resource.objects.all().order_by("-status", "title_eng")
    queryset = models.Resource.objects.order_by("-status", "title_eng").annotate(
        search_term=Concat('title_eng', 'descr_eng', 'purpose_eng', output_field=TextField()))

    # def get_filterset_kwargs(self, filterset_class):
    #     kwargs = super().get_filterset_kwargs(filterset_class)
    #     # if kwargs["data"] is None:
    #     #     kwargs["data"] = {"season": timezone.now().year }
    #     print(kwargs['data'])
    #     return kwargs


class MyResourceListView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login_required/'
    template_name = 'inventory/my_resource_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        custodian_queryset = []
        try:
            custodian_queryset = models.Person.objects.get(pk=self.request.user.id).resource_people.filter(role=1)
        except ObjectDoesNotExist:
            print("Person " + str (self.request.user.id) + "does not exit, Database may be empty")

        context['custodian_list'] = custodian_queryset

        non_custodian_queryset = []
        for resource in models.Resource.objects.filter(people=self.request.user.id):
            add = True
            for resource_person in resource.resource_people.all():
                if resource_person.role.id == 1 and resource_person.person.user_id == self.request.user.id:
                    add = False
            if add == True:
                non_custodian_queryset.append(resource)

        # retain only the unique items, and keep them in order according to keys (cannot use a set for this reason)
        resource_dict = OrderedDict()
        for item in non_custodian_queryset:
            resource_dict[item.id] = item

        # convert the dict back into a list
        non_custodian_list = []
        for item in resource_dict:
            non_custodian_list.append(resource_dict[item])
        context['non_custodian_list'] = non_custodian_list

        context['now'] = timezone.now()

        return context


class ResourceDetailView(DetailView):
    model = models.Resource

    def dispatch(self, request, *args, **kwargs):
        xml_export.verify(models.Resource.objects.get(pk=self.kwargs['pk']))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kcount_other'] = self.object.keywords.filter(
            ~Q(keyword_domain_id=8) & ~Q(keyword_domain_id=6) & ~Q(keyword_domain_id=7) & Q(is_taxonomic=False)).count()
        context['kcount_tc'] = self.object.keywords.filter(keyword_domain_id__exact=8).count()
        context['kcount_cst'] = self.object.keywords.filter(keyword_domain_id__exact=6).count()
        context['kcount_tax'] = self.object.keywords.filter(is_taxonomic__exact=True).count()
        context['kcount_loc'] = self.object.keywords.filter(keyword_domain_id__exact=7).count()
        context['custodian_count'] = self.object.resource_people.filter(role=1).count()
        if self.object.completedness_rating == 1:
            context['verified'] = True
        else:
            context['verified'] = False
        return context


class ResourceFullDetailView(UpdateView):
    model = models.Resource
    form_class = forms.ResourceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readonly'] = True
        return context


class ResourceUpdateView(CustodianRequiredMixin, UpdateView):
    model = models.Resource
    form_class = forms.ResourceForm
    login_url = '/accounts/login_required/'

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
            'date_last_modified': timezone.now(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        resource_list = ['<a href="#id_parent" class="resource_insert" code="{id}" url="{url}">{text}</a>'.format(id=obj.id, text=str(obj),
                                                                                                         url=reverse('inventory:resource_detail',
                                                                                                                     kwargs={'pk': obj.id}))
                         for obj in models.Resource.objects.all()]
        context['resource_list'] = resource_list
        return context


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = models.Resource
    form_class = forms.ResourceCreateForm
    login_url = '/accounts/login_required/'

    def get_initial(self):
        return {
            'last_modified_by': self.request.user,
            'date_last_modified': timezone.now(),
            'add_custodian': True,
            'add_point_of_contact': True,
        }

    def form_valid(self, form):
        object = form.save()
        if form.cleaned_data['add_custodian'] == True:
            models.ResourcePerson.objects.create(resource_id=object.id, person_id=self.request.user.id, role_id=1)

        if form.cleaned_data['add_point_of_contact'] == True:
            models.ResourcePerson.objects.create(resource_id=object.id, person_id=50, role_id=4)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        resource_list = ['<a href="#" class="resource_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                         models.Resource.objects.all()]
        context['resource_list'] = resource_list
        return context


class ResourceDeleteView(CustodianRequiredMixin, DeleteView):
    model = models.Resource
    success_url = reverse_lazy('inventory:resource_list')
    success_message = 'The data resource was successfully deleted!'
    login_url = '/accounts/login_required/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ResourceDeleteFlagUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Resource
    login_url = '/accounts/login_required/'
    template_name = "inventory/resource_flag_deletion.html"
    form_class = forms.ResourceFlagging

    def get_initial(self):
        if self.object.flagged_4_deletion:
            return {
                'flagged_4_deletion': False,
            }
        else:
            return {
                'flagged_4_deletion': True,
            }

    def form_valid(self, form):
        object = form.save()
        if object.flagged_4_deletion:
            email = emails.FlagForDeletionEmail(self.object, self.request.user)
            # send the email object
            if settings.PRODUCTION_SERVER:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print('not sending email since in dev mode')
                print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                                      email.message))

            messages.success(self.request,
                             'The data resource has been flagged for deletion and the regional data manager has been notified!')
        else:
            messages.success(self.request, 'The data resource has been unflagged!')
        return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={"pk": self.kwargs["pk"]}))


class ResourcePublicationFlagUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Resource
    login_url = '/accounts/login_required/'
    template_name = "inventory/resource_flag_publication.html"
    form_class = forms.ResourceFlagging

    def get_initial(self):
        if self.object.flagged_4_publication:
            return {
                'flagged_4_publication': False,
            }
        else:
            return {
                'flagged_4_publication': True,
            }

    def form_valid(self, form):
        object = form.save()
        if object.flagged_4_publication:
            email = emails.FlagForPublicationEmail(self.object, self.request.user)
            # send the email object
            if settings.PRODUCTION_SERVER:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print('not sending email since in dev mode')
                print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                                      email.message))
            messages.success(self.request,
                             'The data resource has been flagged for publication and the regional data manager has been notified!')
        else:
            messages.success(self.request, 'The data resource has been unflagged!')
        return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={"pk": self.kwargs["pk"]}))


# RESOURCE PERSON #
###################

class ResourcePersonFilterView(CustodianRequiredMixin, FilterView):
    filterset_class = filters.PersonFilter
    template_name = "inventory/resource_person_filter.html"

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource

        return context


class ResourcePersonCreateView(CustodianRequiredMixin, CreateView):
    model = models.ResourcePerson
    template_name = 'inventory/resource_person_form.html'
    form_class = forms.ResourcePersonForm

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def get_initial(self):
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        person = models.Person.objects.get(user_id=self.kwargs['person'])
        return {
            'resource': resource,
            'person': person,
            # 'last_modified_by': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = resource
        person = models.Person.objects.get(user_id=self.kwargs['person'])
        context['person'] = person
        return context

    def form_valid(self, form):
        object = form.save()

        # if the person is being added as a custodian
        if object.role.id == 1:
            email = emails.AddedAsCustodianEmail(object.resource, object.person.user)
            # send the email object
            if settings.PRODUCTION_SERVER:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print('not sending email since in dev mode')
                print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                                      email.message))
            messages.success(self.request,
                             '{} has been added as {} and a notification email has been sent to them!'.format(
                                 object.person.full_name, object.role))
        else:
            messages.success(self.request, '{} has been added as {}!'.format(object.person.full_name, object.role))

        return super().form_valid(form)


class ResourcePersonUpdateView(CustodianRequiredMixin, UpdateView):
    model = models.ResourcePerson
    template_name = 'inventory/resource_person_form.html'
    form_class = forms.ResourcePersonForm

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["pk"])

    def form_valid(self, form):
        object = form.save()

        # if the person is being added as a custodian
        if object.role.id == 1:
            email = emails.AddedAsCustodianEmail(object.resource, object.person.user)
            # send the email object
            if settings.PRODUCTION_SERVER:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print('not sending email since in dev mode')
                print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                                      email.message))
            messages.success(self.request,
                             '{} has been added as {} and a notification email has been sent to them!'.format(
                                 object.person.full_name, object.role))
        else:
            messages.success(self.request, '{} has been added as {}!'.format(object.person.full_name, object.role))

        return super().form_valid(form)


class ResourcePersonDeleteView(CustodianRequiredMixin, DeleteView):
    model = models.ResourcePerson
    template_name = 'inventory/resource_person_confirm_delete.html'
    success_url = reverse_lazy('inventory:resource_person')
    success_message = 'The person has been removed from the data resource!'

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        object = models.ResourcePerson.objects.get(pk=self.kwargs["pk"])

        # if the person is being added as a custodian
        if object.role.id == 1:

            email = emails.RemovedAsCustodianEmail(object.resource, object.person.user)
            # send the email object
            if settings.PRODUCTION_SERVER:
                send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                          recipient_list=email.to_list, fail_silently=False, )
            else:
                print('not sending email since in dev mode')
                print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                                      email.message))
            messages.success(self.request,
                             '{} has been removed as {} and a notification email has been sent to them!'.format(
                                 object.person.full_name, object.role))
        else:
            messages.success(self.request, '{} has been removed as {}!'.format(object.person.full_name, object.role))

        # messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('inventory:resource_detail', kwargs={'pk': self.object.resource.id})


# PERSON #
##########

# this is a complicated cookie. Therefore we will not use a model view or model form and handle the clean data manually.
class PersonCreateView(LoginRequiredMixin, FormView):
    template_name = 'inventory/person_form.html'
    form_class = forms.PersonCreateForm

    def get_initial(self):
        return {
            "organization": 6,
        }

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # form.send_email() cool to know you can call methods off of the form like this...

        # step 0: retrieve data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        position_eng = form.cleaned_data['position_eng']
        position_fre = form.cleaned_data['position_fre']
        phone = form.cleaned_data['phone']
        language = form.cleaned_data['language']
        organization = form.cleaned_data['organization']

        # # step 1: create a new user - since we added the receiver decorator to models.py, we do not have to create a person. It will be handled automatically.
        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
            is_active=1,
            email=email,
        )

        # step 2: fetch the Person
        new_person = models.Person.objects.get(user_id=user.id)
        new_person.position_eng = position_eng
        new_person.position_fre = position_fre
        new_person.phone = phone

        if language != "":
            new_person.language = int(language)

        if organization != "":
            new_person.organization_id = organization.id

        new_person.save()

        # finally go to the create new resource person page
        return HttpResponseRedirect(reverse_lazy('inventory:resource_person_add', kwargs={
            'resource': self.kwargs['resource'],
            'person': new_person.user.id,
        }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = resource
        return context


class PersonCreateViewPopout(LoginRequiredMixin, FormView):
    template_name = 'inventory/person_form_popout.html'
    form_class = forms.PersonCreateForm

    def get_initial(self):
        return {
            "organization": 6,
        }

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # form.send_email() cool to know you can call methods off of the form like this...

        # step 0: retrieve data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        position_eng = form.cleaned_data['position_eng']
        position_fre = form.cleaned_data['position_fre']
        phone = form.cleaned_data['phone']
        language = form.cleaned_data['language']
        organization = form.cleaned_data['organization']

        # # step 1: create a new user - since we added the receiver decorator to models.py, we do not have to create a person. It will be handled automatically.
        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
            is_active=1,
            email=email,
        )

        # step 2: fetch the Person
        new_person = models.Person.objects.get(user_id=user.id)
        new_person.position_eng = position_eng
        new_person.position_fre = position_fre
        new_person.phone = phone

        if language != "":
            new_person.language = int(language)

        if organization != "":
            new_person.organization = organization

        new_person.save()

        # finally close the form
        return HttpResponseRedirect(reverse_lazy('inventory:close_me'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PersonUpdateView(LoginRequiredMixin, FormView):
    template_name = 'inventory/person_form.html'
    form_class = forms.PersonForm

    def get_success_url(self):
        try:
            self.kwargs['resource']
        except KeyError:
            print("no resource id")
            return reverse_lazy('inventory:my_resource_list')
        else:
            return reverse_lazy('inventory:resource_detail', kwargs={
                'pk': self.kwargs['resource'],
            })

    def get_initial(self):
        person = models.Person.objects.get(pk=self.kwargs['person'])
        return {
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'email': person.user.email,
            'position_eng': person.position_eng,
            'position_fre': person.position_fre,
            'phone': person.phone,
            'language': person.language,
            'organization': person.organization_id,
        }

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        old_person = models.Person.objects.get(pk=self.kwargs['person'])

        # step 0: retreive data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        position_eng = form.cleaned_data['position_eng']
        position_fre = form.cleaned_data['position_fre']
        phone = form.cleaned_data['phone']
        language = form.cleaned_data['language']
        organization = form.cleaned_data['organization']

        # step 2: Retrieve the Person model
        old_person.user.first_name = first_name
        old_person.user.last_name = last_name
        old_person.user.email = email
        old_person.user.username = email

        old_person.position_eng = position_eng
        old_person.position_fre = position_fre
        old_person.phone = phone

        if language == "" or language is None:
            old_person.language = None
        else:
            old_person.language = int(language)

        if organization == "" or organization is None:
            old_person.organization_id = None
        else:
            old_person.organization = organization

        old_person.user.save()
        old_person.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            resource = models.Resource.objects.get(id=self.kwargs['resource'])
            context['resource'] = resource
        except KeyError:
            print("no resource id")

        person = models.Person.objects.get(user_id=self.kwargs['person'])
        context['person'] = person
        return context


# RESOURCE KEYWORD #
####################


class ResourceKeywordFilterView(CustodianRequiredMixin, FilterView):
    filterset_class = filters.KeywordFilter
    template_name = "inventory/resource_keyword_filter.html"
    queryset = models.Keyword.objects.annotate(
        search_term=Concat('text_value_eng', Value(' '), 'details', output_field=TextField())).filter(
        ~Q(keyword_domain_id=8) & ~Q(keyword_domain_id=6) & ~Q(keyword_domain_id=7) & Q(is_taxonomic=False)).order_by(
        'text_value_eng')

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        context['keyword_type'] = "Keyword"
        return context


class ResourceTopicCategoryFilterView(FilterView):
    filterset_class = filters.KeywordFilter
    template_name = "inventory/resource_keyword_filter.html"
    queryset = models.Keyword.objects.annotate(
        search_term=Concat('text_value_eng', Value(' '), 'details', output_field=TextField())).filter(
        keyword_domain_id__exact=8).order_by('text_value_eng')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        context['keyword_type'] = "Topic Category"
        return context


class ResourceCoreSubjectFilterView(FilterView):
    filterset_class = filters.KeywordFilter
    template_name = "inventory/resource_keyword_filter.html"
    queryset = models.Keyword.objects.annotate(
        search_term=Concat('text_value_eng', Value(' '), 'details', output_field=TextField())).filter(
        keyword_domain_id__exact=6).order_by('text_value_eng')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        context['keyword_type'] = "Core Subject"
        return context


class ResourceSpeciesFilterView(FilterView):
    filterset_class = filters.KeywordFilter
    template_name = "inventory/resource_keyword_filter.html"
    queryset = models.Keyword.objects.annotate(
        search_term=Concat('text_value_eng', Value(' '), 'details', output_field=TextField())).filter(
        is_taxonomic=True).order_by('text_value_eng')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        context['keyword_type'] = "Taxonomic Keyword"
        return context


class ResourceLocationFilterView(FilterView):
    filterset_class = filters.KeywordFilter
    template_name = "inventory/resource_keyword_filter.html"
    queryset = models.Keyword.objects.annotate(
        search_term=Concat('text_value_eng', Value(' '), 'details', output_field=TextField())).filter(
        keyword_domain_id__exact=7).order_by('text_value_eng')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        context['keyword_type'] = "DFO Area"
        return context


def resource_keyword_add(request, resource, keyword, keyword_type):
    my_keyword = models.Keyword.objects.get(pk=keyword)
    my_resource = models.Resource.objects.get(pk=resource)

    if my_resource.keywords.filter(pk=keyword).count() > 0:
        messages.warning(request, "'{}' has already been added as a keyword.".format(my_keyword.text_value_eng))
    else:
        my_resource.keywords.add(keyword)
        messages.success(request, "'{}' has been added as a keyword.".format(my_keyword.text_value_eng))

    if keyword_type == "topic-category":
        return HttpResponseRedirect(reverse('inventory:resource_topic_category_filter', kwargs={'resource': resource}))
    elif keyword_type == "core-subject":
        return HttpResponseRedirect(reverse('inventory:resource_core_subject_filter', kwargs={'resource': resource}))
    elif keyword_type == "taxonomic-keyword":
        return HttpResponseRedirect(reverse('inventory:resource_species_filter', kwargs={'resource': resource}))
    elif keyword_type == "keyword":
        return HttpResponseRedirect(reverse('inventory:resource_keyword_filter', kwargs={'resource': resource}))
    elif keyword_type == "dfo-area":
        return HttpResponseRedirect(reverse('inventory:resource_location_filter', kwargs={'resource': resource}))


def resource_keyword_delete(request, resource, keyword):
    my_keyword = models.Keyword.objects.get(pk=keyword)
    my_resource = models.Resource.objects.get(pk=resource)

    my_resource.keywords.remove(keyword)
    messages.success(request, "'{}' has been removed.".format(my_keyword.text_value_eng))

    return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': resource}))


# KEYWORD #
###########

class KeywordDetailView(DetailView):
    model = models.Keyword

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context


class KeywordUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Keyword
    form_class = forms.KeywordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context

    def get_success_url(self):
        return reverse_lazy('inventory:keyword_detail', kwargs={
            'resource': self.kwargs['resource'],
            'pk': self.kwargs['pk'],
        })


class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = models.Keyword
    form_class = forms.KeywordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context

    def form_valid(self, form):
        self.object = form.save()
        my_resource = models.Resource.objects.get(pk=self.kwargs['resource']).keywords.add(self.object.id)
        messages.success(self.request, "'{}' has been added as a keyword.".format(self.object.text_value_eng))
        return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': self.kwargs['resource']}))


def keyword_delete(request, resource, keyword):
    my_keyword = models.Keyword.objects.get(pk=keyword)
    my_keyword.delete()
    messages.success(request, "'{}' has been removed from the database.".format(my_keyword.text_value_eng))
    return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': resource}))


# RESOURCE CITATION #
####################

class ResourceCitationFilterView(FilterView):
    filterset_class = filters.CitationFilter
    template_name = "inventory/resource_citation_filter.html"
    queryset = models.Citation.objects.annotate(
        search_term=Concat('title_eng', Value(' '), 'title_fre', Value(' '), 'pub_number', Value(' '), 'year',
                           Value(' '), 'series', output_field=TextField())).order_by('title_eng')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.kwargs['resource']
        my_resource = models.Resource.objects.get(id=resource)
        context['resource'] = my_resource
        return context


def resource_citation_add(request, resource, citation):
    my_citation = models.Citation.objects.get(pk=citation)
    my_resource = models.Resource.objects.get(pk=resource)

    if my_resource.citations.filter(pk=citation).count() > 0:
        messages.warning(request, "'{}' has already been added as a citation.".format(my_citation.title))
    else:
        my_resource.citations.add(citation)
        messages.success(request, "'{}' has been added as a citation.".format(my_citation.title))

    return HttpResponseRedirect(reverse('inventory:resource_citation_filter', kwargs={'resource': resource}))


def resource_citation_delete(request, resource, citation):
    my_citation = models.Citation.objects.get(pk=citation)
    my_resource = models.Resource.objects.get(pk=resource)

    my_resource.citations.remove(citation)
    messages.success(request, "'{}' has been removed.".format(my_citation.title))

    return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': resource}))


# CITATION #
############

class CitationDetailView(DetailView):
    model = models.Citation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context


class CitationUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Citation
    form_class = forms.CitationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context

    def get_success_url(self):
        return reverse_lazy('inventory:citation_detail', kwargs={
            'resource': self.kwargs['resource'],
            'pk': self.kwargs['pk'],
        })


class CitationCreateView(LoginRequiredMixin, CreateView):
    model = models.Citation
    form_class = forms.CitationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(id=self.kwargs['resource'])
        context['resource'] = my_resource
        return context

    def form_valid(self, form):
        self.object = form.save()
        my_resource = models.Resource.objects.get(pk=self.kwargs['resource']).citations.add(self.object.id)
        messages.success(self.request, "'{}' has been added as a citation.".format(self.object.title))
        return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': self.kwargs['resource']}))

@login_required(login_url='/accounts/login_required/')
def citation_delete(request, resource, citation):
    my_citation = models.Citation.objects.get(pk=citation)
    my_citation.delete()
    messages.success(request, "'{}' has been removed from the database.".format(my_citation.title))
    return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk': resource}))


# PUBLICATION #
###############

class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = models.Publication
    fields = "__all__"
    login_url = '/accounts/login_required/'
    template_name = 'inventory/publication_form_popout.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('inventory:close_me'))


# XML GOODNESS #
################

def export_resource_xml(request, resource, publish):
    # grab resource instance
    my_resource = models.Resource.objects.get(pk=resource)

    if publish == "yes":
        my_resource.fgp_publication_date = timezone.now()
        my_resource.flagged_4_publication = False

        my_resource.save()

    # Create the HttpResponse object
    filename = "xml_metadata_export_{}.xml".format(my_resource.id)
    response = HttpResponse(content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    # pass the object to the xml builder module
    xml_data = xml_export.construct(my_resource)

    response.write(xml_data)
    # print(xml_data)
    return response
    # return HttpResponseRedirect(reverse('inventory:resource_detail', kwargs={'pk':resource}))


# DATA MANAGEMENT ADMIN #
#########################

class DataManagementHomeTemplateView(InventoryDMRequiredMixin, TemplateView):
    template_name = 'inventory/dm_admin_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        published_records = models.Resource.objects.filter(fgp_publication_date__isnull=False).count()
        context["published_records"] = published_records

        flagged_4_deletion = models.Resource.objects.filter(flagged_4_deletion=True).count()
        context["flagged_4_deletion"] = flagged_4_deletion

        flagged_4_publication = models.Resource.objects.filter(flagged_4_publication=True).count()
        context["flagged_4_publication"] = flagged_4_publication

        return context


class DataManagementCustodianListView(InventoryDMRequiredMixin, TemplateView):
    login_url = '/accounts/login_required/'
    template_name = 'inventory/dm_custodian_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = models.ResourcePerson.objects.filter(role=1).order_by("person__user__last_name",
                                                                         "person__user__first_name")

        # retain only the unique items, and keep them in order according to keys (cannot use a set for this reason)
        custodian_dict = OrderedDict()
        for item in queryset:
            custodian_dict[item.person.user_id] = item

        # convert the dict back into a list
        custodian_list = []
        for item in custodian_dict:
            custodian_list.append(custodian_dict[item])

        context['custodian_list'] = custodian_list
        context['custodian_count'] = len(custodian_list)

        context['now'] = timezone.now()

        return context


class DataManagementCustodianDetailView(InventoryDMRequiredMixin, DetailView):
    login_url = '/accounts/login_required/'
    template_name = 'inventory/dm_custodian_detail.html'
    model = models.Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object.resource_people.filter(role=1)
        me = models.Person.objects.get(user=User.objects.get(pk=self.request.user.id))
        email = emails.CertificationRequestEmail(me, self.object)
        context['queryset'] = queryset
        context['email'] = email
        context['now'] = timezone.now()
        # context['custodian_count'] = len(custodian_list)
        return context


def send_certification_request(request, person):
    # grab a copy of the resource
    my_person = models.Person.objects.get(pk=person)
    # create a new email object
    me = models.Person.objects.get(user=User.objects.get(pk=self.request.user.id))
    email = emails.CertificationRequestEmail(me, my_person)
    # send the email object
    if settings.PRODUCTION_SERVER:
        send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                  recipient_list=email.to_list, fail_silently=False, )
    else:
        print('not sending email since in dev mode')
        print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                              email.message))

    my_person.user.correspondences.create(subject="Request for certification")
    messages.success(request, "the email has been sent and the correspondence has been logged!")
    return HttpResponseRedirect(reverse('inventory:dm_custodian_detail', kwargs={'pk': my_person.user_id}))


class PublishedResourcesListView(InventoryDMRequiredMixin, ListView):
    template_name = "inventory/dm_published_resource.html"
    queryset = models.Resource.objects.filter(fgp_publication_date__isnull=False)


class FlaggedListView(InventoryDMRequiredMixin, ListView):
    template_name = "inventory/dm_flagged_list.html"

    def get_queryset(self):
        if self.kwargs["flag_type"] == "publication":
            queryset = models.Resource.objects.filter(flagged_4_publication=True)
        elif self.kwargs["flag_type"] == "deletion":
            queryset = models.Resource.objects.filter(flagged_4_deletion=True)
        return queryset


class CertificationListView(InventoryDMRequiredMixin, ListView):
    template_name = "inventory/dm_certification_list.html"
    queryset = models.ResourceCertification.objects.all().order_by("-certification_date")[:50]


class ModificationListView(InventoryDMRequiredMixin, ListView):
    template_name = "inventory/dm_modification_list.html"
    queryset = models.Resource.objects.all().order_by("-date_last_modified")[:50]


class CustodianPersonUpdateView(InventoryDMRequiredMixin, FormView):
    template_name = 'inventory/dm_custodian_form.html'
    form_class = forms.PersonCreateForm

    def get_success_url(self):
        return reverse_lazy('inventory:dm_custodian_detail', kwargs={
            'pk': self.kwargs['person'],
        })

    def get_initial(self):
        person = models.Person.objects.get(pk=self.kwargs['person'])
        return {
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'email': person.user.email,
            'position_eng': person.position_eng,
            'position_fre': person.position_fre,
            'phone': person.phone,
            'language': person.language,
            'organization': person.organization.id,
        }

    def form_valid(self, form):
        old_person = models.Person.objects.get(pk=self.kwargs['person'])

        # step 0: retreive data from form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        position_eng = form.cleaned_data['position_eng']
        position_fre = form.cleaned_data['position_fre']
        phone = form.cleaned_data['phone']
        language = form.cleaned_data['language']
        organization = form.cleaned_data['organization']

        # step 2: Retrieve the Person model
        old_person.user.first_name = first_name
        old_person.user.last_name = last_name
        old_person.user.email = email
        old_person.user.username = email

        old_person.position_eng = position_eng
        old_person.position_fre = position_fre
        old_person.phone = phone

        if language != "":
            old_person.language = int(language)

        if organization != "":
            old_person.organization_id = int(organization)

        old_person.user.save()
        old_person.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = models.Person.objects.get(user_id=self.kwargs['person'])
        context['person'] = person
        return context


## SECTIONS

class SectionListView(InventoryDMRequiredMixin, ListView):
    template_name = "inventory/dm_section_list.html"
    queryset = shared_models.Section.objects.all().order_by("division__branch__region", "division__branch", "division", "name")


class SectionDetailView(InventoryDMRequiredMixin, DetailView):
    template_name = "inventory/dm_section_detail.html"
    model = shared_models.Section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.head:
            me = models.Person.objects.get(user=self.request.user)
            email = emails.SectionReportEmail(me, self.object.head, self.object)
            context['email'] = email
        context['now'] = timezone.now()
        return context


def send_section_report(request, section):
    # grab a copy of the resource
    my_section = shared_models.Section.objects.get(pk=section)
    head = my_section.head
    # create a new email object
    me = models.Person.objects.get(user=request.user)
    email = emails.SectionReportEmail(me, head, my_section)
    # send the email object
    if settings.PRODUCTION_SERVER:
        send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                  recipient_list=email.to_list, fail_silently=False, )
    else:
        print('not sending email since in dev mode')
        print("FROM={}; TO={}; SUBJECT={}; MESSAGE={}".format(email.from_email, email.to_list, email.subject,
                                                              email.message))

    models.Correspondence.objects.create(custodian=head.user, subject="Section head report")
    messages.success(request, "the email has been sent and the correspondence has been logged!")
    return HttpResponseRedirect(reverse('inventory:dm_section_detail', kwargs={'pk': section}))


class MySectionDetailView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/my_section_detail.html"
    model = shared_models.Section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # grab the user
        user_id = self.request.user.id
        my_section = shared_models.Section.objects.filter(head_id=user_id).first()

        if my_section:
            resource_list = my_section.resources.all().order_by("title_eng")
            context['resource_list'] = resource_list

            ## NOTE if there is ever a need to have a person with two sections under them, this view will have to be modified so that a list of sections is returned to the user.
            # Would simply have to remove the first() function from my_section

            context['object'] = my_section
            context['now'] = timezone.now()

            certified_within_year = 0
            certified_within_6_months = 0
            for r in my_section.resources.all():
                try:
                    days_elapsed = (timezone.now() - r.certification_history.order_by(
                        "-certification_date").first().certification_date).days
                except Exception as e:
                    print(e)
                else:
                    if days_elapsed < 183:  # six months
                        certified_within_6_months = certified_within_6_months + 1
                        certified_within_year = certified_within_year + 1
                    elif days_elapsed < 365:
                        certified_within_year = certified_within_year + 1

            context['certified_within_6_months'] = certified_within_6_months
            context['certified_within_year'] = certified_within_year

            published_on_fgp = 0
            for r in my_section.resources.all():
                if r.fgp_publication_date:  # six months
                    published_on_fgp = published_on_fgp + 1

            context['published_on_fgp'] = published_on_fgp

        return context


# RESOURCE CERTIFICATION #
##########################


class ResourceCertificationCreateView(CustodianRequiredMixin, CreateView):
    model = models.ResourceCertification
    template_name = 'inventory/resource_certification_form.html'
    form_class = forms.ResourceCertificationForm
    success_message = "Certification successful!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_resource = models.Resource.objects.get(pk=self.kwargs['pk'])

        context['resource'] = my_resource
        return context

    def get_initial(self):
        return {
            'certifying_user': self.request.user,
            'resource': self.kwargs['pk'],
            'certification_date': timezone.now(),
        }

    def get_success_url(self):
        return reverse('inventory:resource_detail', kwargs={
            'pk': self.kwargs['pk'],
        })

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class ResourceCertificationDeleteView(CustodianRequiredMixin, DeleteView):
    model = models.ResourceCertification
    template_name = 'inventory/resource_certification_confirm_delete.html'
    success_message = "The certification event has been removed."

    def get_success_url(self):
        return reverse('inventory:resource_detail', kwargs={
            'pk': self.object.resource.id,
        })

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# FILES #
#########

class FileCreateView(CustodianRequiredMixin, CreateView):
    template_name = "inventory/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("inventory:resource_detail", kwargs={"pk": object.resource.id}))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        context["resource"] = resource
        return context

    def get_initial(self):
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        return {'resource': resource}


class FileDetailView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context


class FileUpdateView(CustodianRequiredMixin, UpdateView):
    template_name = "inventory/file_form.html"
    model = models.File
    form_class = forms.FileForm

    def test_func(self):
        my_object = models.File.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context


class FileDeleteView(CustodianRequiredMixin, DeleteView):
    template_name = "inventory/file_confirm_delete.html"
    model = models.File

    def test_func(self):
        my_object = models.File.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})


# DATA RESOURCE #
#################

class DataResourceCreateView(CustodianRequiredMixin, CreateView):
    template_name = "inventory/data_resource_form.html"
    model = models.DataResource
    form_class = forms.DataResourceForm

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("inventory:resource_detail", kwargs={"pk": object.resource.id}))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        context["resource"] = resource
        return context

    def get_initial(self):
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        return {'resource': resource}


class DataResourceUpdateView(CustodianRequiredMixin, UpdateView):
    template_name = "inventory/data_resource_form.html"
    model = models.DataResource
    form_class = forms.DataResourceForm

    def test_func(self):
        my_object = models.DataResource.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        return context


class DataResourceDeleteView(CustodianRequiredMixin, DeleteView):
    template_name = "inventory/data_resource_confirm_delete.html"
    model = models.DataResource

    def test_func(self):
        my_object = models.DataResource.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})


# WEB SERVICES #
################

class WebServiceCreateView(CustodianRequiredMixin, CreateView):
    template_name = "inventory/data_resource_form.html"
    model = models.WebService
    form_class = forms.WebServiceForm

    def test_func(self):
        return is_custodian_or_admin(self.request.user, self.kwargs["resource"])

    def form_valid(self, form):
        object = form.save()
        return HttpResponseRedirect(reverse_lazy("inventory:resource_detail", kwargs={"pk": object.resource.id}))

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        context["resource"] = resource
        return context

    def get_initial(self):
        resource = models.Resource.objects.get(pk=self.kwargs['resource'])
        return {'resource': resource}


class WebServiceUpdateView(CustodianRequiredMixin, UpdateView):
    template_name = "inventory/data_resource_form.html"
    model = models.WebService
    form_class = forms.WebServiceForm

    def test_func(self):
        my_object = models.WebService.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        return context


class WebServiceDeleteView(CustodianRequiredMixin, DeleteView):
    template_name = "inventory/data_resource_confirm_delete.html"
    model = models.WebService

    def test_func(self):
        my_object = models.WebService.objects.get(pk=self.kwargs["pk"])
        return is_custodian_or_admin(self.request.user, my_object.resource_id)

    def get_success_url(self, **kwargs):
        return reverse_lazy("inventory:resource_detail", kwargs={"pk": self.object.resource.id})


# REPORTS #
###########

class ReportSearchFormView(InventoryDMRequiredMixin, FormView):
    template_name = 'inventory/report_search.html'
    form_class = forms.ReportSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        sections = str(form.cleaned_data["sections"]).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")

        if sections == "":
            sections = "None"

        if report == 1:
            return HttpResponseRedirect(reverse("inventory:export_batch_xml", kwargs={
                'sections': sections,
            }))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("inventory:report_search"))


def export_batch_xml(request, sections):
    file_url = reports.generate_batch_xml(sections)
    print(file_url)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename="xml_batch_export_{}.zip"'.format(
                timezone.now().strftime("%Y-%m-%d"))
            return response
    raise Http404

    # return HttpResponseRedirect(reverse("inventory:report_search"))

# def capacity_export_spreadsheet(request, fy=None, orgs=None):
#     file_url = reports.generate_capacity_spreadsheet(fy, orgs)
#
#     if os.path.exists(file_url):
#         with open(file_url, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename="iHub export {}.xlsx"'.format(timezone.now().strftime("%Y-%m-%d"))
#             return response
#     raise Http404
