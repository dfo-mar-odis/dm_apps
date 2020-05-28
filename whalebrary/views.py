from django.utils.text import slugify
from django.utils.translation import gettext as _

from lib.functions.custom_functions import listrify
from shared_models import models as shared_models
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count, TextField, F, Sum
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from django.utils import timezone
from . import models
from . import forms
from . import filters
from . import reports


class CloserTemplateView(TemplateView):
    template_name = 'whalebrary/close_me.html'

### Permissions ###

class WhalebraryAccessRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)

def in_whalebrary_admin_group(user):
    if "whalebrary_admin" in [g.name for g in user.groups.all()]:
        return True

class WhalebraryAdminAccessRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login_required/'

    def test_func(self):
        return in_whalebrary_admin_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


def in_whalebrary_edit_group(user):
    """this group includes the admin group so there is no need to add an admin to this group"""
    if user:
        if in_whalebrary_admin_group(user) or user.groups.filter(name='whalebrary_edit').count() != 0:
            return True

class WhalebraryEditRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return in_whalebrary_edit_group(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login_required/')
def index(request):
    return render(request, 'whalebrary/index.html')


# #
# # INVENTORY #
# # ###########
# #
#
class ItemListView(WhalebraryAccessRequired, FilterView):
    template_name = "whalebrary/item_list.html"
    filterset_class = filters.SpecificItemFilter
    queryset = models.Item.objects.annotate(
        search_term=Concat('item_name', 'description', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Item.objects.first()
        context["field_list"] = [
            'id',
            'tname|{}'.format(_("Item name (size)")),
            'description',
            'serial_number',
            'owner',
            # 'size',
            'category',
            'gear_type',
            'suppliers',
            'last_purchased',
            'last_purchased_by',
        ]
        return context


class ItemDetailView(WhalebraryAccessRequired, DetailView):
    model = models.Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'item_name',
            'description',
            'serial_number',
            'owner',
            'size',
            'category',
            'gear_type',
            'suppliers',
            'last_purchased',
            'last_purchased_by',

        ]

        # contexts for _quantity.html file
        context["random_qty"] = models.Quantity.objects.first()
        context["qty_field_list"] = [
            'quantity',
            'status',
            'location',
            'bin_id',
        ]

               # now when you create a new item you get this error:   context['quantity_avail'] = ohqty - lentqty
        # TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType' -- have to add a case where there is
        # no info yet in those fields? -- fixed it I think~!!! WOOOOH

        ohqty = self.get_object().quantities.filter(status=1).aggregate(dsum=Sum('quantity')).get('dsum')
        lentqty = self.get_object().quantities.filter(status=3).aggregate(dsum=Sum('quantity')).get('dsum')

        if ohqty is None:
            ohqty = 0
        else:
            ohqty = ohqty

        if lentqty is None:
            lentqty = 0
        else:
            lentqty = lentqty

        context['quantity_avail'] = ohqty - lentqty

        # context for _supplier.html
        context["random_sup"] = models.Supplier.objects.first()
        context["sup_field_list"] = [
            'supplier_name',
            'contact_number',
            'email',

        ]


        # context for _lending.html
        context["random_lend"] = models.Quantity.objects.first()
        context["lend_field_list"] = [
            'lent_to',
            'quantity',
            'lent_date',
            'return_date',
        ]

        # context for _files.html
        context["random_file"] = models.File.objects.first()
        context["file_field_list"] = [
            'caption',
            'file',
            'date_uploaded',
        ]

        return context


class ItemUpdateView(WhalebraryEditRequiredMixin, UpdateView):
    model = models.Item
    form_class = forms.ItemForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Item record successfully updated for : {my_object}"))
        return super().form_valid(form)


class ItemCreateView(WhalebraryEditRequiredMixin, CreateView):
    model = models.Item
    form_class = forms.ItemForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Item record successfully created for : {my_object}"))
        return super().form_valid(form)


class ItemDeleteView(WhalebraryEditRequiredMixin, DeleteView):
    model = models.Item
    permission_required = "__all__"
    success_url = reverse_lazy('whalebrary:item_list')
    success_message = 'The item was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

        ## LOCATION ##

class LocationListView(WhalebraryAdminAccessRequired, FilterView):
    template_name = "whalebrary/location_list.html"
    filterset_class = filters.LocationFilter
    queryset = models.Location.objects.annotate(
        search_term=Concat('location', 'address', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Location.objects.first()
        context["field_list"] = [
            'id',
            'location',
            'address',
            'container',
            'container_space',

        ]
        return context

class LocationDetailView(WhalebraryAdminAccessRequired, DetailView):
    model = models.Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'location',
            'address',
            'container',
            'container_space',

        ]
        return context

class LocationUpdateView(WhalebraryAdminAccessRequired, UpdateView):
    model = models.Location
    form_class = forms.LocationForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Location record successfully updated for : {my_object}"))
        return super().form_valid(form)

class LocationCreateView(WhalebraryAdminAccessRequired, CreateView):
    model = models.Location
    form_class = forms.LocationForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Location record successfully created for : {my_object}"))
        return super().form_valid(form)

class LocationDeleteView(WhalebraryAdminAccessRequired, DeleteView):
    model = models.Location
    permission_required = "__all__"
    success_url = reverse_lazy('whalebrary:location_list')
    success_message = 'The location file was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    ##QUANTITY##


class QuantityListView(WhalebraryAccessRequired, FilterView):
    template_name = "whalebrary/quantity_list.html"
    filterset_class = filters.QuantityFilter
    queryset = models.Quantity.objects.annotate(
        search_term=Concat('id', 'item', 'quantity', 'status', 'lent_to', 'lent_date', 'return_date', 'last_audited', 'last_audited_by', 'location', 'bin_id',
                           output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Quantity.objects.first()
        context["field_list"] = [
            'id',
            'item',
            'quantity',
            'status',
            'lent_to',
            'lent_date',
            'return_date',
            'last_audited',
            'last_audited_by',
            'location',
            'bin_id',
        ]
        return context


class QuantityDetailView(WhalebraryAccessRequired, DetailView):
    model = models.Quantity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'item',
            'quantity',
            'status',
            'lent_to',
            'lent_date',
            'return_date',
            'last_audited',
            'last_audited_by',
            'location',
            'bin_id',
        ]

        return context


class QuantityUpdateView(WhalebraryEditRequiredMixin, UpdateView):
    model = models.Quantity
    form_class = forms.QuantityForm

    def get_template_names(self):
       return "whalebrary/quantity_form_popout.html" if self.kwargs.get("pop") else "whalebrary/quantity_form.html"

    def get_form_class(self):
        return forms.QuantityForm1 if self.kwargs.get("pop") else forms.QuantityForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Quantity record successfully updated for : {my_object}"))
        success_url = reverse_lazy('shared_models:close_me') if self.kwargs.get("pop") else reverse_lazy('whalebrary:quantity_detail', kwargs={"pk": my_object.id})
        return HttpResponseRedirect(success_url)


class QuantityCreateView(WhalebraryEditRequiredMixin, CreateView):
    model = models.Quantity
    form_class = forms.QuantityForm

    def get_template_names(self):
       return "whalebrary/quantity_form_popout.html" if self.kwargs.get("pk") else "whalebrary/quantity_form.html"

    def get_form_class(self):
        return forms.QuantityForm1 if self.kwargs.get("pk") else forms.QuantityForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Quantity record successfully created for : {my_object}"))
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me') if self.kwargs.get("pk") else reverse_lazy('whalebrary:quantity_list'))


    def get_initial(self):
        return {'item': self.kwargs.get('pk')}


class QuantityDeleteView(WhalebraryEditRequiredMixin, DeleteView):
    model = models.Quantity
    permission_required = "__all__"
    success_message = 'The quantity was successfully deleted!'

    def get_template_names(self):
        return "whalebrary/generic_confirm_delete_popout.html" if self.kwargs.get("pop") else "whalebrary/quantity_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me') if self.kwargs.get("pop") else reverse_lazy('whalebrary:quantity_list'))

    ##BULK QUANTITY##

class BulkQuantityListView(WhalebraryAdminAccessRequired, FilterView):
    filterset_class = filters.BulkQuantityFilter
    template_name = 'whalebrary/bulk_quantity_list.html'
    queryset = models.Quantity.objects.annotate(
        search_term=Concat('id', 'item__item_name', 'quantity', 'status', 'lent_to', 'lent_date', 'return_date', 'location', 'bin_id',
                           output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Quantity.objects.first()
        context["field_list"] = [
            'id',
            'item',
            'quantity',
            'status',
            'lent_to',
            'lent_date',
            'return_date',
            'location',
            'bin_id',
        ]
        return context

# from https://github.com/ccnmtl/dmt/blob/master/dmt/main/views.py#L614
# class BulkQuantityDetailView(WhalebraryAdminAccessRequired, DetailView):
#     model = models.Quantity #or should this be Quantity? TBD
#
#     @staticmethod
#     def reassign_status(request, quantities, new_status):
#         item_names = []
#         for pk in quantities:
#             item = get_object_or_404(models.Quantity, pk=pk)
#             item.reassign(request.quantity.status, new_status, '')
#             item_names.append(
#                 '<a href="{}">{}</a>'.format(
#                     item.get_absolute_url(), item.item_name))
#
#         if len(item_names) > 0:
#             msg = 'Assigned the following items to ' + \
#                   '<strong>{}</strong>: {}'.format(
#                       new_status.get_fullname(),
#                       ', '.join(item_names))
#             messages.success(request, mark_safe(msg))
#
#     def post(self, request, *args, **kwargs):
#         action = request.POST.get('action')
#         quantities = request.POST.getlist('_selected_action')
#
#         if action == 'edit' and request.POST.get('edit_status'):
#             edit_status = request.POST.get('edit_status')
#             status = get_object_or_404(Status, name=edit_status)
#             self.reassign_status(request, quantities, status)
#
#         return HttpResponseRedirect(
#             reverse('bulk_quantity_detail', args=args, kwargs=kwargs))


class BulkQuantityDeleteView(WhalebraryAdminAccessRequired, DeleteView):
    model = models.Quantity
    permission_required = "__all__"
    success_url = reverse_lazy('whalebrary:bulk_quantity_list')
    success_message = 'The quantity was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    ## PERSONNEL ##


class PersonnelListView(WhalebraryAdminAccessRequired, FilterView):
    template_name = "whalebrary/personnel_list.html"
    filterset_class = filters.PersonnelFilter
    queryset = models.Personnel.objects.annotate(
        search_term=Concat('id', 'first_name', 'last_name', 'organisation', 'email', 'phone', 'exp_level', 'training',
                           output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Personnel.objects.first()
        context["field_list"] = [
            'id',
            'first_name',
            'last_name',
            'organisation',
            'email',
            'phone',
            'exp_level',
            'training',

        ]
        return context


class PersonnelDetailView(WhalebraryAdminAccessRequired, DetailView):
    model = models.Personnel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'first_name',
            'last_name',
            'organisation',
            'email',
            'phone',
            'exp_level',
            'training',

        ]
        return context


class PersonnelUpdateView(WhalebraryAdminAccessRequired, UpdateView):
    model = models.Personnel
    form_class = forms.PersonnelForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Personnel record successfully updated for : {my_object}"))
        return super().form_valid(form)


class PersonnelCreateView(WhalebraryAdminAccessRequired, CreateView):
    model = models.Personnel
    form_class = forms.PersonnelForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Personnel record successfully created for : {my_object}"))
        return super().form_valid(form)


class PersonnelDeleteView(WhalebraryAdminAccessRequired, DeleteView):
    model = models.Personnel
    permission_required = "__all__"
    success_url = reverse_lazy('whalebrary:personnel_list')
    success_message = 'The personnel file was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    ## SUPPLIER ##


class SupplierListView(WhalebraryAccessRequired, FilterView):
    template_name = "whalebrary/supplier_list.html"
    filterset_class = filters.SupplierFilter
    queryset = models.Supplier.objects.annotate(
        search_term=Concat('id', 'supplier_name', 'contact_number', 'email', 'website', 'comments',
                           output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Supplier.objects.first()
        context["field_list"] = [
            'id',
            'supplier_name',
            'contact_number',
            'email',
            'website',
            'comments',

        ]
        return context


class SupplierDetailView(WhalebraryAccessRequired, DetailView):
    model = models.Supplier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'supplier_name',
            'contact_number',
            'email',
            'website',
            'comments',
        ]
        return context


class SupplierUpdateView(WhalebraryEditRequiredMixin, UpdateView):
    model = models.Supplier
    form_class = forms.SupplierForm

    def get_template_names(self):
       return "whalebrary/supplier_form_popout.html" if self.kwargs.get("pop") else "whalebrary/supplier_form.html"

    def get_form_class(self):
        return forms.SupplierForm1 if self.kwargs.get("pop") else forms.SupplierForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Supplier record successfully updated for : {my_object}"))
        success_url = reverse_lazy('shared_models:close_me') if self.kwargs.get("pop") else reverse_lazy('whalebrary:supplier_detail', kwargs={"pk": my_object.id})
        return HttpResponseRedirect(success_url)

class SupplierCreateView(WhalebraryEditRequiredMixin, CreateView):
    model = models.Supplier
    form_class = forms.SupplierForm

    def get_template_names(self):
       return "whalebrary/supplier_form_popout.html" if self.kwargs.get("pk") else "whalebrary/supplier_form.html"

    def get_form_class(self):
        return forms.SupplierForm1 if self.kwargs.get("pk") else forms.SupplierForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Supplier record successfully created for : {my_object}"))

        #if there's a pk argumentm this means user is calling from item_detail page and
        if self.kwargs.get("pk"):
            my_item = models.Item.objects.get(pk=self.kwargs.get("pk"))
            my_item.suppliers.add(my_object)
            return HttpResponseRedirect(reverse_lazy('shared_models:close_me'))
        else:
            return HttpResponseRedirect(reverse_lazy('whalebrary:supplier_list'))

    def get_initial(self):
        return {'item': self.kwargs.get('pk')}

class SupplierDeleteView(WhalebraryEditRequiredMixin, DeleteView):
    model = models.Supplier
    permission_required = "__all__"
    success_message = 'The supplier file was successfully deleted!'

    def get_template_names(self):
        return "whalebrary/generic_confirm_delete_popout.html" if self.kwargs.get("pop") else "whalebrary/supplier_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me') if self.kwargs.get("pop") else reverse_lazy('whalebrary:supplier_list'))

    ## ITEM FILE UPLOAD ##


class FileCreateView(WhalebraryEditRequiredMixin, CreateView):
    model = models.File
    template_name = 'whalebrary/file_form_popout.html'
    form_class = forms.FileForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"File successfully added for : {my_object}"))
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me'))

    def get_initial(self):
        item = models.Item.objects.get(pk=self.kwargs['item'])
        return {
            'item': item,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        context["item"] = models.Item.objects.get(pk=self.kwargs.get("item"))
        return context


class FileUpdateView(WhalebraryEditRequiredMixin, UpdateView):
    model = models.File
    template_name = 'whalebrary/file_form_popout.html'
    form_class = forms.FileForm

    def get_context_data(self, **kwargs):
        # get context
        context = super().get_context_data(**kwargs)
        context["editable"] = True
        return context

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"File record successfully updated for : {my_object}"))
        success_url = reverse_lazy('shared_models:close_me')
        return HttpResponseRedirect(success_url)


class FileDetailView(FileUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editable"] = False
        return context

class FileDeleteView(WhalebraryEditRequiredMixin, DeleteView):
    model = models.File
    permission_required = "__all__"
    success_message = 'The file was successfully deleted!'

    def get_template_names(self):
        return "whalebrary/generic_confirm_delete_popout.html"

    def delete(self, request, *args, **kwargs):
        my_object = self.get_object()
        my_object.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(reverse_lazy('shared_models:close_me'))


    ## INCIDENT ##


class IncidentListView(WhalebraryAccessRequired, FilterView):
    template_name = "whalebrary/incident_list.html"
    filterset_class = filters.IncidentFilter
    queryset = models.Incident.objects.annotate(
        search_term=Concat('id', 'species_count', 'submitted', 'first_report', 'location', 'region', output_field=TextField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Incident.objects.first()
        context["field_list"] = [
            'id',
            'species_count',
            'submitted',
            'first_report',
            'location',
            'region',
            'incident_type',
            'exam',

        ]
        return context


class IncidentDetailView(WhalebraryAccessRequired, DetailView):
    model = models.Incident

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = [
            'id',
            'species_count',
            'submitted',
            'first_report',
            'lat',
            'long',
            'location',
            'region',
            'species',
            'sex',
            'age_group',
            'incident_type',
            'gear_presence',
            'gear_desc',
            'exam',
            'necropsy',
            'results',
            'photos',
            'data_folder',
            'comments',

        ]
        return context


class IncidentUpdateView(WhalebraryEditRequiredMixin, UpdateView):
    model = models.Incident
    form_class = forms.IncidentForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Incident record successfully updated for : {my_object}"))
        return super().form_valid(form)


class IncidentCreateView(WhalebraryEditRequiredMixin, CreateView):
    model = models.Incident
    form_class = forms.IncidentForm

    def form_valid(self, form):
        my_object = form.save()
        messages.success(self.request, _(f"Incident record successfully created for : {my_object}"))
        return super().form_valid(form)


class IncidentDeleteView(WhalebraryEditRequiredMixin, DeleteView):
    model = models.Incident
    permission_required = "__all__"
    success_url = reverse_lazy('whalebrary:incident_list')
    success_message = 'The incident file was successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


    ## REPORTS ##

class ReportGeneratorFormView(WhalebraryAccessRequired, FormView):
    template_name = 'whalebrary/report_generator.html'

    form_class = forms.ReportGeneratorForm

    def get_initial(self):

        try:
            self.kwargs["report_number"]
        except KeyError:
            print("no report")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        report = int(form.cleaned_data["report"])

        try:
            location = int(form.cleaned_data["location"])
        except ValueError:
            location = None
        try:
            item_name = slugify(form.cleaned_data["item_name"])
        except ValueError:
            item_name = None

        if report == 1:
            return HttpResponseRedirect(reverse("whalebrary:report_container", kwargs={
                'location': str(location),
            }))
        elif report == 2:
            return HttpResponseRedirect(reverse("whalebrary:report_sized_item", kwargs={'item_name': item_name}))

        else:
            messages.error(self.request, "Report is not available. Please select another report.")
            return HttpResponseRedirect(reverse("whalebrary:report_generator"))


class ContainerSummaryListView(WhalebraryAccessRequired, ListView):
    template_name = 'whalebrary/report_container_summary.html'

    def get_queryset(self, **kwargs):
        qs = models.Quantity.objects.filter(location_id=self.kwargs['location'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Quantity.objects.first()

        context["field_list"] = [
            'item',
            'quantity',
            'status',
            'lent_to',
            'lent_date',
            'return_date',
            'last_audited',
            'last_audited_by',
        ]

        return context

class SizedItemSummaryListView(WhalebraryAccessRequired, ListView):
    template_name = 'whalebrary/report_sized_item_summary.html'

    def get_queryset(self, **kwargs):
        qs = models.Quantity.objects.filter(item__item_name__iexact=self.kwargs['item_name'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_object"] = models.Quantity.objects.first()

        context["field_list"] = [
            'item',
            'quantity',
            'status',
            'lent_to',
            'lent_date',
            'return_date',
            'last_audited',
            'last_audited_by',
            'location',
            'bin_id',
        ]

        return context