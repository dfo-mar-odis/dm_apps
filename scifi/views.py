import csv
import datetime
import json

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from dm_apps.utils import custom_send_mail
from django.db.models import TextField, Sum, Value
from django.db.models.functions import Concat
from django.utils import timezone
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, FormView, TemplateView
###
import os

from lib.functions.custom_functions import fiscal_year
from lib.functions.custom_functions import nz
from . import models
from . import forms
from . import filters
from . import reports
from . import emails
from shared_models import models as shared_models


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'scifi/close_me.html'


def in_scifi_admin_group(user):
    if user:
        return user.groups.filter(name='scifi_admin').count() != 0


def is_logged_in(user):
    # a quick check to see if user is logged in
    if user.id:
        return True


def can_modify(user, transaction_id):
    """returns True if user is allowed to edit a transaction. This would be the case if
    1) the transaction was created by the user
    2) they are a scifi user who is allowed to interact with the transaction's RC
     """

    if user.id:
        # get the instance of the transaction
        my_trans = models.Transaction.objects.get(pk=transaction_id)

        # check to see if user created the transaction
        if my_trans.created_by == user:
            return True
        else:
            # if the user has no associated scifi user in the app, automatic fail
            try:
                scifi_user = models.SciFiUser.objects.get(user=user)
            except ObjectDoesNotExist:
                return False
            else:
                # check to see if the transaction RC is listed in the scifi user rc list
                return my_trans.responsibility_center in [rc for rc in scifi_user.responsibility_centers.all()]


class SciFiAccessRequiredMixin(LoginRequiredMixin):
    # everyone who is logged in should be able to access scifi
    login_url = '/accounts/login/'


class OnlyThoseAllowedToEditMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return can_modify(self.request.user, self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:denied_access"))
        return super().dispatch(request, *args, **kwargs)


class SciFiAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):


    def test_func(self):
        return in_scifi_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SciFiAccessRequiredMixin, TemplateView):
    template_name = 'scifi/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_user = self.request.user
        rc_list = shared_models.ResponsibilityCenter.objects.filter(manager=my_user)
        context["rc_list"] = rc_list
        context["fy"] = fiscal_year(sap_style=True)

        return context


# SCIFI USERS #
###############

class SciFiUserListView(SciFiAccessRequiredMixin, ListView):
    model = models.SciFiUser
    template_name = 'scifi/scifiuser_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'user',
            'responsibility_centers',
        ]
        context["my_object"] = self.model.objects.first()
        return context


class SciFiUserUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = models.SciFiUser
    form_class = forms.SciFiUserForm
    success_url = reverse_lazy('scifi:user_list')
    template_name = 'scifi/scifiuser_form.html'


class SciFiUserCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.SciFiUser
    form_class = forms.SciFiUserForm
    success_url = reverse_lazy('scifi:user_list')
    template_name = 'scifi/scifiuser_form.html'


class SciFiUserDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = models.SciFiUser
    success_url = reverse_lazy('scifi:user_list')
    success_message = 'The scifi user was successfully deleted!'
    template_name = 'scifi/scifiuser_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ALLOTMENT CODE #
##################

class AllotmentCodeListView(SciFiAccessRequiredMixin, ListView):
    queryset = shared_models.AllotmentCode.objects.all().order_by("allotment_category", "code")
    template_name = 'scifi/allotmentcode_list.html'


class AllotmentCodeUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = shared_models.AllotmentCode
    form_class = forms.AllotmentCodeForm
    success_url = reverse_lazy('scifi:allotment_list')
    template_name = 'scifi/allotmentcode_form.html'


class AllotmentCodeCreateView(SciFiAdminRequiredMixin, CreateView):
    model = shared_models.AllotmentCode
    form_class = forms.AllotmentCodeForm
    success_url = reverse_lazy('scifi:allotment_list')
    template_name = 'scifi/allotmentcode_form.html'


class AllotmentCodeDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = shared_models.AllotmentCode
    success_url = reverse_lazy('scifi:allotment_list')
    success_message = 'The allotment code was successfully deleted!'
    template_name = 'scifi/allotmentcode_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AllotmentCodeDetailView(SciFiAccessRequiredMixin, DetailView):
    model = shared_models.AllotmentCode
    template_name = 'scifi/allotmentcode_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
            'allotment_category',
        ]
        return context


# BUSINESS LINE #
#################

class BusinessLineListView(SciFiAccessRequiredMixin, ListView):
    model = shared_models.BusinessLine
    template_name = 'scifi/businessline_list.html'


class BusinessLineUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = shared_models.BusinessLine
    form_class = forms.BusinessLineForm
    success_url = reverse_lazy('scifi:business_list')
    template_name = 'scifi/businessline_form.html'


class BusinessLineCreateView(SciFiAdminRequiredMixin, CreateView):
    model = shared_models.BusinessLine
    form_class = forms.BusinessLineForm
    success_url = reverse_lazy('scifi:business_list')
    template_name = 'scifi/businessline_form.html'


class BusinessLineDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = shared_models.BusinessLine
    success_url = reverse_lazy('scifi:business_list')
    success_message = 'The business line was successfully deleted!'
    template_name = 'scifi/businessline_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class BusinessLineDetailView(SciFiAccessRequiredMixin, DetailView):
    model = shared_models.BusinessLine
    template_name = 'scifi/businessline_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
        ]
        return context


# LINE OBJECT #
###############

class LineObjectListView(SciFiAccessRequiredMixin, FilterView):
    template_name = 'scifi/lineobject_list.html'
    filterset_class = filters.LineObjectFilter
    model = shared_models.LineObject
    queryset = shared_models.LineObject.objects.annotate(
        search_term=Concat('code', 'name_eng', 'description_eng', output_field=TextField()))


class LineObjectUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = shared_models.LineObject
    form_class = forms.LineObjectForm
    success_url = reverse_lazy('scifi:lo_list')
    template_name = 'scifi/lineobject_form.html'


class LineObjectCreateView(SciFiAdminRequiredMixin, CreateView):
    model = shared_models.LineObject
    form_class = forms.LineObjectForm
    success_url = reverse_lazy('scifi:lo_list')
    template_name = 'scifi/lineobject_form.html'


class LineObjectDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = shared_models.LineObject
    success_url = reverse_lazy('scifi:lo_list')
    success_message = 'The line object was successfully deleted!'
    template_name = 'scifi/lineobject_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class LineObjectDetailView(SciFiAdminRequiredMixin, DetailView):
    model = shared_models.LineObject
    template_name = 'scifi/lineobject_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name_eng',
            'description_eng',
        ]
        return context


# RC #
######

class ResponsibilityCentreListView(SciFiAccessRequiredMixin, ListView):
    model = shared_models.ResponsibilityCenter
    template_name = 'scifi/responsibilitycenter_list.html'


class ResponsibilityCentreUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = shared_models.ResponsibilityCenter
    form_class = forms.ResponsibilityCentreForm
    success_url = reverse_lazy('scifi:rc_list')
    template_name = 'scifi/responsibilitycenter_form.html'


class ResponsibilityCentreCreateView(SciFiAdminRequiredMixin, CreateView):
    model = shared_models.ResponsibilityCenter
    form_class = forms.ResponsibilityCentreForm
    success_url = reverse_lazy('scifi:rc_list')
    template_name = 'scifi/responsibilitycenter_form.html'


class ResponsibilityCentreDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = shared_models.ResponsibilityCenter
    success_url = reverse_lazy('scifi:rc_list')
    success_message = 'The RC was successfully deleted!'
    template_name = 'scifi/responsibilitycenter_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ResponsibilityCentreDetailView(SciFiAccessRequiredMixin, DetailView):
    model = shared_models.ResponsibilityCenter
    template_name = 'scifi/responsibilitycenter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'code',
            'name',
            'manager',
        ]
        return context


# PROJECT #
###########

class ProjectListView(SciFiAccessRequiredMixin, FilterView):
    filterset_class = filters.LineObjectFilter
    template_name = 'scifi/project_list.html'
    queryset = shared_models.Project.objects.annotate(
        search_term=Concat('code', 'name', 'description', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name',
            'code',
            'description',
            'project_lead',
            'default_responsibility_center.code',
            'default_allotment_code.code',
            'default_business_line.code',
            'default_line_object.code',
        ]
        return context


class ProjectUpdateView(SciFiAdminRequiredMixin, UpdateView):
    model = shared_models.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy('scifi:project_list')
    template_name = 'scifi/project_form.html'


class ProjectCreateView(SciFiAdminRequiredMixin, CreateView):
    model = shared_models.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy('scifi:project_list')
    template_name = 'scifi/project_form.html'


class ProjectDeleteView(SciFiAdminRequiredMixin, DeleteView):
    model = shared_models.Project
    success_url = reverse_lazy('scifi:project_list')
    success_message = 'The project was successfully deleted!'
    template_name = 'scifi/project_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ProjectDetailView(SciFiAccessRequiredMixin, DetailView):
    model = shared_models.Project
    template_name = 'scifi/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'name',
            'code',
            'description',
            'project_lead',
            'default_responsibility_center',
            'default_allotment_code',
            'default_business_line',
            'default_line_object',
        ]
        return context


# TRANSACTION #
###############

class TransactionListView(SciFiAccessRequiredMixin, FilterView):
    template_name = 'scifi/transaction_list.html'
    filterset_class = filters.TransactionFilter
    model = models.Transaction
    queryset = models.Transaction.objects.annotate(
        search_term=Concat(
            'supplier_description',
            Value(" "),
            'reference_number',
            Value(" "),
            'comment',
            Value(" "),
            'consignee_code__code',
            Value("-"),
            'consignee_suffix',
            output_field=TextField()
        )
    )

    # paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'fiscal_year',
            'responsibility_center.code',
            'business_line.code',
            'allotment_code',
            'line_object.code',
            'project.code',
            'transaction_type',
            'supplier_description',
            'creation_date',
            'expected_purchase_date',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'reference_number',
            'regional_f_number|Regional consignee code',
            'invoice_date',
            'in_mrs',
            'amount_paid_in_mrs',
            'mrs_notes',
            'procurement_hub_contact',
            'exclude_from_rollup',
            'comment',
        ]
        context["my_object"] = self.model.objects.first()
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {
                "fiscal_year": fiscal_year(sap_style=True),
            }
        return kwargs


class TransactionBasicListView(SciFiAccessRequiredMixin, FilterView):
    template_name = 'scifi/transaction_basic_list.html'
    filterset_class = filters.TransactionFilter
    model = models.Transaction

    # paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'fiscal_year',
            'responsibility_center.code',
            'business_line.code',
            'allotment_code.code',
            'line_object.code',
            'project.code',
            'transaction_type',
            'supplier_description',
            'creation_date',
            'expected_purchase_date',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'reference_number',
            'invoice_date',
            # 'in_mrs',
            # 'amount_paid_in_mrs',
            # 'mrs_notes',
            # 'procurement_hub_contact',
            # 'comment',
        ]
        context["my_object"] = self.model.objects.first()
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {
                "fiscal_year": fiscal_year(),
            }
        return kwargs


@login_required(login_url='/accounts/login/')
@user_passes_test(in_scifi_admin_group, login_url='/accounts/denied/')
def toggle_mrs(request, pk, query=None):
    # get instance of transaction
    my_t = models.Transaction.objects.get(pk=pk)

    if my_t.in_mrs:
        my_t.in_mrs = False
    else:
        my_t.in_mrs = True
    my_t.save()

    return HttpResponseRedirect(reverse("scifi:trans_list") + "?{}#trans{}".format(query, pk))


class TransactionDetailView(SciFiAccessRequiredMixin, DetailView):
    model = models.Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'fiscal_year',
            'responsibility_center',
            'business_line',
            'allotment_code',
            'line_object',
            'project',
            'transaction_type',
            'supplier_description',
            'creation_date',
            'expected_purchase_date',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'reference_number',
            'regional_f_number|Regional consignee code',
            'invoice_date',
            'in_mrs',
            'amount_paid_in_mrs',
            'mrs_notes',
            'procurement_hub_contact',
            'exclude_from_rollup',
            'comment',
            'created_by',
        ]
        return context


class TransactionUpdateView(OnlyThoseAllowedToEditMixin, UpdateView):
    model = models.Transaction
    form_class = forms.TransactionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        shared_models.Project.objects.all()]
        context['project_list'] = project_list

        return context


class TransactionDuplicateView(TransactionUpdateView):

    def get_initial(self):
        # This is I think where we'll want to intercept if we need to change some thing from the record being duplicated
        init = super().get_initial()
        init["creation_date"] = timezone.now()
        init["created_by"] = self.request.user
        return init

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.pk = None
        obj.save()

        return HttpResponseRedirect(reverse_lazy("scifi:trans_detail", kwargs={"pk": obj.id}))

    def test_func(self):
        # this view should be available to any user
        return is_logged_in(self.request.user)


class TransactionCreateView(SciFiAdminRequiredMixin, CreateView):
    model = models.Transaction
    form_class = forms.TransactionForm

    def get_initial(self):
        return {
            'fiscal_year': fiscal_year(sap_style=True),
            'created_by': self.request.user,
            'do_another': 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        shared_models.Project.objects.all()]
        context['project_list'] = project_list

        return context

    def form_valid(self, form):
        object = form.save()
        if form.cleaned_data["do_another"] == 1:
            return HttpResponseRedirect(reverse_lazy('scifi:trans_new'))
        else:
            return HttpResponseRedirect(reverse_lazy('scifi:trans_list'))


class TransactionDeleteView(OnlyThoseAllowedToEditMixin, DeleteView):
    model = models.Transaction
    success_url = reverse_lazy('scifi:trans_list')
    success_message = 'The transaction was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


## CUSTOM TRANSACTIONS

class CustomTransactionCreateView(SciFiAccessRequiredMixin, CreateView):
    model = models.Transaction
    form_class = forms.CustomTransactionForm
    template_name = "scifi/transaction_form.html"

    def get_initial(self):
        return {
            'fiscal_year': fiscal_year(sap_style=True),
            'created_by': self.request.user,
            'transaction_type': 3,
            'in_mrs': False,
            'do_another': 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_transaction'] = True

        # get lists
        rc_list = ['<a href="#" class="rc_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.ResponsibilityCenter.objects.all()]
        context['rc_list'] = rc_list

        bl_list = ['<a href="#" class="bl_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.BusinessLine.objects.all()]
        context['bl_list'] = bl_list

        ac_list = ['<a href="#" class="ac_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.AllotmentCode.objects.all()]
        context['ac_list'] = ac_list

        lo_list = ['<a href="#" class="lo_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for obj in
                   shared_models.LineObject.objects.all()]
        context['lo_list'] = lo_list

        project_list = ['<a href="#" class="project_insert" code={id}>{text}</a>'.format(id=obj.id, text=str(obj)) for
                        obj in
                        shared_models.Project.objects.all()]
        context['project_list'] = project_list

        # project dict for default coding
        project_dict = {}
        for project in shared_models.Project.objects.all():
            project_dict[project.id] = {}
            project_dict[project.id]["rc"] = project.default_responsibility_center_id
            project_dict[project.id]["bl"] = project.default_business_line_id
            project_dict[project.id]["ac"] = project.default_allotment_code_id
            project_dict[project.id]["lo"] = project.default_line_object_id

        project_json = json.dumps(project_dict)
        # send JSON file to template so that it can be used by js script
        context['project_json'] = project_json

        return context

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewEntryEmail(self.object, self.request)
        # send the email object
        if email.to_list:
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )

        if form.cleaned_data["do_another"] == 1:
            return HttpResponseRedirect(reverse_lazy('scifi:ctrans_new'))
        else:
            return HttpResponseRedirect(reverse_lazy('scifi:index'))


# IMPORT FILE

class ImportFileView(SciFiAdminRequiredMixin, CreateView):
    model = models.TempFile
    fields = ["temp_file", ]
    template_name = 'scifi/file_import_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        header_dict = {
            "FISCAL YEAR": [
                "MANDATORY",
                'integer field',
                'SAP format',
                "e.g., 2019-2019 should be entered in as '2020'",
            ],
            "RC": [
                "MANDATORY",
                "5-digit integer field",
            ],
            "BUSINESS LINE": [
                "MANDATORY",
                '3-digit integer field',
            ],
            "ALLOTMENT CODE": [
                "MANDATORY",
                'string field',
                "e.g., 120, 120-, 485*, 36V",
                "not case sensitive",
            ],
            "LINE OBJECT": ['string field', "e.g., T515, 3239", "not case sensitive", "leave blank if null"],
            "PROJECT CODE": [
                "MANDATORY",
                'string field',
                "e.g., 71026x, 71RD7",
                "not case sensitive",
                "leave blank if null",
            ],
            "TRANSACTION TYPE": [
                'string field',
                "must be one of the following: 'expenditure', 'allocation' or 'adjustment'",
                "not case sensitive",
                "if blank, will default to expenditure",
            ],
            "DESCRIPTION": ['text field', ],
            "OBLIGATION COST": ["number field", ],
            "INVOICE COST": ["number field", ],
            "IN MRS": ['string field', "must be one of the following: 'yes', or 'no'",
                       "not case sensitive", "If left blank, it will default to 'No'"],
            "REFERENCE NUMBER": ['text field', ],
            "INVOICE DATE": ['date field', "must be formated as 'MM/DD/YYYY'"],
            "EXPECTED PURCHASE DATE": ['date field', "must be formated as 'MM/DD/YYYY'"],
        }
        context["header_dict"] = header_dict
        return context

    def form_valid(self, form):
        my_object = form.save()
        # now we need to do some magic with the file...

        # load the file
        url = self.request.META.get("HTTP_ORIGIN") + my_object.temp_file.url
        r = requests.get(url)
        csv_reader = csv.DictReader(r.text.splitlines())

        # for each make a new polygon
        i = 1
        for row in csv_reader:
            print(i)
            # try to do the import, if not throw a message back to the user.

            try:
                # TRANSACTION TYPE
                if row.get("TRANSACTION TYPE"):
                    if "adjust" in row.get("TRANSACTION TYPE").lower():
                        my_type = 2
                    elif "allot" in row.get("TRANSACTION TYPE").lower():
                        my_type  = 1
                    else:
                        my_type  = 3
                else:
                    my_type  = 3

                # IN MRS
                if row.get("IN MRS"):
                    if row.get("IN MRS").lower() == "yes":
                        in_mrs = True
                    else:
                        in_mrs  = False
                else:
                    in_mrs  = False

                # INVOICE DATE
                invoice_date = datetime.datetime.strptime(row.get("INVOICE DATE"), "%m/%d/%Y") if row.get("INVOICE DATE") else None

                # EXPECTED PURCHASE DATE
                expected_purchase_date = datetime.datetime.strptime(row.get("EXPECTED PURCHASE DATE"), "%m/%d/%Y") if row.get("EXPECTED PURCHASE DATE") else None

                # LINE OBJECT
                if row.get("LINE OBJECT"):
                    try:
                        lo = shared_models.LineObject.objects.get(code=row.get("LINE OBJECT"))
                    except shared_models.LineObject.DoesNotExist:
                        lo = None
                else:
                    lo = None

                my_t = models.Transaction.objects.create(
                    fiscal_year=shared_models.FiscalYear.objects.get(pk=row.get("FISCAL YEAR")),
                    responsibility_center=shared_models.ResponsibilityCenter.objects.get(code=row.get("RC")),
                    business_line=shared_models.BusinessLine.objects.get(code=row.get("BUSINESS LINE")),
                    allotment_code=shared_models.AllotmentCode.objects.get(code=row.get("ALLOTMENT CODE")),
                    project=shared_models.Project.objects.get(code=row.get("PROJECT CODE")),

                    # OPTIONAL FIELDS
                    line_object=lo,
                    transaction_type=my_type,
                    supplier_description=row.get("DESCRIPTION"),
                    obligation_cost=float(row.get("OBLIGATION COST")),
                    invoice_cost=float(row.get("INVOICE COST")),
                    in_mrs=in_mrs,
                    reference_number=row.get("REFERENCE NUMBER"),
                    invoice_date=invoice_date,
                    expected_purchase_date=expected_purchase_date,
                )
                my_t.created_by = self.request.user
                my_t.save()

            except Exception as e:
                print(e)
                messages.error(self.request, "Problem importing transaction on line {} of csv file.".format(i))

            i += 1

        # clear the file in my object
        my_object.temp_file = None
        my_object.save()
        return HttpResponseRedirect(reverse_lazy('scifi:trans_list'))


# REPORTS #
###########

class ReportSearchFormView(SciFiAccessRequiredMixin, FormView):
    template_name = 'scifi/report_search.html'

    form_class = forms.ReportSearchForm

    def get_initial(self):
        # default the year to the year of the latest samples
        my_dict = {
            "fiscal_year": fiscal_year(sap_style=True),
        }

        try:
            self.kwargs["report_number"]
        except KeyError:
            print("no report")
        else:
            my_dict["report"] = self.kwargs["report_number"]

        return my_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        fiscal_year = int(form.cleaned_data["fiscal_year"])
        report = int(form.cleaned_data["report"])
        try:
            rc = int(form.cleaned_data["rc"])
        except ValueError:
            rc = None
        try:
            project = int(form.cleaned_data["project"])
        except ValueError:
            project = None

        if report == 1:
            return HttpResponseRedirect(reverse("scifi:report_master", kwargs={
                'fy': fiscal_year,
                'rc': str(rc),
                'project': str(project),
            }))

        elif report == 2:
            return HttpResponseRedirect(reverse("scifi:report_rc", kwargs={'fiscal_year': fiscal_year, "rc": rc}))
        elif report == 3:
            return HttpResponseRedirect(reverse("scifi:report_project", kwargs={
                'fiscal_year': fiscal_year,
                'project': project,
            }))
        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("scifi:report_search"))


class AccountSummaryTemplateView(SciFiAccessRequiredMixin, TemplateView):
    template_name = 'scifi/report_rc_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs['fiscal_year'])
        context["fiscal_year"] = fy

        rc = shared_models.ResponsibilityCenter.objects.get(pk=self.kwargs['rc'])
        context["rc"] = rc

        project_list = [shared_models.Project.objects.get(pk=rc["project"]) for rc in
                        models.Transaction.objects.filter(fiscal_year=fy).filter(
                            responsibility_center=rc.id).values(
                            "project").order_by("project").distinct() if
                        rc["project"] is not None]
        context["project_list"] = project_list

        ac_list = [shared_models.AllotmentCode.objects.get(pk=t["allotment_code"]) for t in
                   models.Transaction.objects.filter(fiscal_year=fy).filter(
                       responsibility_center=rc.id).values(
                       "allotment_code").order_by("allotment_code").distinct()]
        context["ac_list"] = ac_list

        # will have to make a custom dictionary to send in
        my_dict = {}
        total_obligations = {}
        total_expenditures = {}
        total_allocations = {}
        total_adjustments = {}

        for ac in ac_list:
            total_obligations[ac.code] = 0
            total_expenditures[ac.code] = 0
            total_allocations[ac.code] = 0
            total_adjustments[ac.code] = 0

        for p in project_list:
            my_dict[p.code] = {}
            my_dict[p.code]["allocations"] = 0
            my_dict[p.code]["adjustments"] = 0
            my_dict[p.code]["obligations"] = 0
            my_dict[p.code]["expenditures"] = 0
            my_dict[p.code]["rcs"] = str(
                [rc["responsibility_center__code"] for rc in models.Transaction.objects.filter(project=p).values(
                    "responsibility_center__code").order_by("responsibility_center__code").distinct()]).replace("'",
                                                                                                                "").replace(
                "[", "").replace("]", "")
            my_dict[p.code]["ac_cats"] = str([rc["allotment_code__allotment_category__name"] for rc in
                                              models.Transaction.objects.filter(project=p).values(
                                                  "allotment_code__allotment_category__name").order_by(
                                                  "allotment_code").distinct()]).replace("'", "").replace("[",
                                                                                                          "").replace(
                "]", "")

            for ac in ac_list:

                # project allocation
                try:
                    project_allocations = \
                        nz(models.Transaction.objects.filter(
                            project_id=p.id,
                            exclude_from_rollup=False,
                            fiscal_year=fy,
                            transaction_type=1,
                            allotment_code=ac
                        ).values("invoice_cost").order_by("invoice_cost").aggregate(dsum=Sum("invoice_cost"))["dsum"], 0)
                except TypeError:
                    project_allocations = 0

                my_dict[p.code]["allocations"] += project_allocations

                # total allocations
                ## must be done by allotment code
                total_allocations[ac.code] += project_allocations

                # project adjustments
                try:
                    project_adjustments = \
                        nz(models.Transaction.objects.filter(
                            project_id=p.id,
                            exclude_from_rollup=False,
                            fiscal_year=fy,
                            transaction_type=2,
                            allotment_code=ac
                        ).values("invoice_cost").order_by("invoice_cost").aggregate(dsum=Sum("invoice_cost"))["dsum"], 0)
                except TypeError:
                    project_adjustments = 0

                my_dict[p.code]["adjustments"] += project_adjustments
                # total allocations
                total_adjustments[ac.code] += project_adjustments

                # project obligations
                try:
                    project_obligations = \
                        nz(models.Transaction.objects.filter(
                            project_id=p.id,
                            exclude_from_rollup=False,
                            fiscal_year=fy,
                            transaction_type=3,
                            allotment_code=ac
                        ).values("outstanding_obligation").order_by("outstanding_obligation").aggregate(dsum=Sum("outstanding_obligation"))[
                               "dsum"], 0)
                except TypeError:
                    project_obligations = 0

                my_dict[p.code]["obligations"] += project_obligations
                # total obligations
                total_obligations[ac.code] += project_obligations

                # project expenditures
                try:
                    project_expenditures = \
                        nz(models.Transaction.objects.filter(
                            project_id=p.id,
                            exclude_from_rollup=False,
                            fiscal_year=fy,
                            transaction_type=3,
                            allotment_code=ac
                        ).values("invoice_cost").order_by("invoice_cost").aggregate(dsum=Sum("invoice_cost"))["dsum"], 0)
                except TypeError:
                    project_expenditures = 0

                my_dict[p.code]["expenditures"] += project_expenditures
                # total expenditures
                total_expenditures[ac.code] += project_expenditures

        my_dict["total_obligations"] = total_obligations
        my_dict["total_expenditures"] = total_expenditures
        my_dict["total_adjustments"] = total_adjustments
        my_dict["total_allocations"] = total_allocations
        context["my_dict"] = my_dict

        return context


class ProjectSummaryListView(SciFiAccessRequiredMixin, ListView):
    template_name = 'scifi/report_project_summary.html'

    def get_queryset(self, **kwargs):
        qs = models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(
            fiscal_year_id=self.kwargs["fiscal_year"]).order_by("-transaction_type", "creation_date")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Transaction.objects.first()
        fy = shared_models.FiscalYear.objects.get(pk=self.kwargs['fiscal_year'])
        context["fiscal_year"] = fy

        project = shared_models.Project.objects.get(pk=self.kwargs['project'])
        context["project"] = project

        context["field_list"] = [
            'fiscal_year',
            'creation_date',
            'responsibility_center.code',
            'allotment_code',
            'transaction_type',
            'obligation_cost',
            'invoice_cost',
            'outstanding_obligation',
            'supplier_description',
        ]

        # will have to make a custom dictionary to send in
        my_dict = {}
        my_dict["total_allocations"] = {}
        my_dict["total_adjustments"] = {}
        my_dict["total_obligations"] = {}
        my_dict["total_expenditures"] = {}

        qs = models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(fiscal_year=fy)

        ac_list = [shared_models.AllotmentCode.objects.get(pk=t["allotment_code"]) for t in
                   qs.values("allotment_code").order_by("allotment_code").distinct()]
        context["ac_list"] = ac_list

        for ac in ac_list:
            # project allocation
            try:
                project_allocations = \
                    nz(models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(
                        fiscal_year=fy).filter(
                        transaction_type=1).filter(allotment_code=ac).values("project").order_by(
                        "project").aggregate(dsum=Sum("invoice_cost"))["dsum"], 0)
            except TypeError:
                project_allocations = 0

            my_dict["total_allocations"][ac.code] = project_allocations

            # project adjustments
            try:
                project_adjustments = \
                    models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(
                        fiscal_year=fy).filter(
                        transaction_type=2).filter(allotment_code=ac).values(
                        "project").order_by("project").aggregate(dsum=Sum("invoice_cost"))["dsum"]
            except TypeError:
                project_adjustments = 0

            my_dict["total_adjustments"][ac.code] = project_adjustments

            # project obligations
            try:
                project_obligations = \
                    models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(
                        fiscal_year=fy).filter(transaction_type=3).filter(allotment_code=ac).values(
                        "project").order_by("project").aggregate(
                        dsum=Sum("outstanding_obligation"))["dsum"]
            except TypeError:
                project_obligations = 0

            my_dict["total_obligations"][ac.code] = project_obligations

            # project expenditures
            try:
                project_expenditures = \
                    nz(models.Transaction.objects.filter(project_id=self.kwargs["project"]).filter(exclude_from_rollup=False).filter(
                        fiscal_year=fy).filter(
                        transaction_type=3).filter(allotment_code=ac).values(
                        "project").order_by("project").aggregate(dsum=Sum("invoice_cost"))[
                           "dsum"], 0)
            except TypeError:
                project_expenditures = 0

            my_dict["total_expenditures"][ac.code] = project_expenditures

        context["my_dict"] = my_dict
        return context


def master_spreadsheet(request, fy, rc, project):
    file_url = reports.generate_master_spreadsheet(fy, rc, project)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="transactions export ({}).xlsx"'.format(
                timezone.now().strftime("%y-%m-%d"))
            return response
    raise Http404
