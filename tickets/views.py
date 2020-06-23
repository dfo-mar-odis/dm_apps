from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _, gettext_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, DetailView, ListView
from django_filters.views import FilterView
from shutil import copyfile
from github import Github

import os

from dm_apps.utils import custom_send_mail
from shared_models.views import CommonFilterView, CommonDetailView, CommonUpdateView, CommonDeleteView, CommonCreateView, \
    CommonPopoutCreateView, CommonPopoutUpdateView, CommonPopoutDeleteView, CommonPopoutDetailView
from . import models
from . import forms
from . import filters
from . import reports
from . import emails


def index_router(request):
    # if the user is a staff user, then go to my_tickets
    if request.user.id:
        print("there is a user")
        if request.user.is_staff:
            # go to assigned tickets
            return HttpResponseRedirect(reverse("tickets:my_assigned_list"))
        else:
            # go to 'my tickets'
            return HttpResponseRedirect(reverse("tickets:my_list"))
    else:
        # no user. go to all tickets
        return HttpResponseRedirect(reverse("tickets:list"))


# Ticket #
##########
class TicketListView(LoginRequiredMixin, CommonFilterView):
    filterset_class = filters.TicketFilter
    template_name = "tickets/list.html"
    queryset = models.Ticket.objects.annotate(
        search_term=Concat('id', 'title', 'description', 'notes', output_field=TextField()))
    h1 = gettext_lazy("Data Management Tickets")
    container_class = "container-fluid"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'priority', "class": "", "width": ""},
        {"name": 'dm_assigned', "class": "", "width": ""},
        {"name": 'app_display|app', "class": "", "width": ""},
        {"name": 'title', "class": "", "width": ""},
        {"name": 'request_type', "class": "", "width": ""},
        {"name": 'section', "class": "", "width": ""},
        {"name": 'status', "class": "", "width": ""},
        {"name": 'primary_contact', "class": "", "width": ""},
        {"name": 'sd_ref_number', "class": "", "width": ""},
    ]


class MyTicketListView(LoginRequiredMixin, CommonFilterView):
    filterset_class = filters.MyTicketFilter
    template_name = "tickets/list.html"
    new_object_url_name = "tickets:create"
    row_object_url_name = "tickets:detail"
    container_class = "container-fluid"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'priority', "class": "", "width": ""},
        {"name": 'dm_assigned', "class": "", "width": ""},
        {"name": 'app_display|app', "class": "", "width": ""},
        {"name": 'title', "class": "", "width": ""},
        {"name": 'request_type', "class": "", "width": ""},
        {"name": 'section', "class": "", "width": ""},
        {"name": 'status', "class": "", "width": ""},
        {"name": 'primary_contact', "class": "", "width": ""},
        {"name": 'sd_ref_number', "class": "", "width": ""},
    ]

    def get_h1(self):
        return f"{self.request.user.first_name}'s Tickets"

    def get_queryset(self):
        return models.Ticket.objects.filter(primary_contact=self.request.user).annotate(
            search_term=Concat('id', 'title', 'description', 'notes', output_field=TextField()))

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {"status": 2, }
        return kwargs


class MyAssignedTicketListView(LoginRequiredMixin, CommonFilterView):
    filterset_class = filters.MyTicketFilter
    template_name = "tickets/list.html"
    new_object_url_name = "tickets:create"
    row_object_url_name = "tickets:detail"
    container_class = "container-fluid"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'primary_contact', "class": "", "width": ""},
        {"name": 'priority', "class": "", "width": ""},
        {"name": 'dm_assigned', "class": "", "width": ""},
        {"name": 'app_display|app', "class": "", "width": ""},
        {"name": 'title', "class": "", "width": ""},
        {"name": 'request_type', "class": "", "width": ""},
        {"name": 'status', "class": "", "width": ""},
        {"name": 'github_issue_number', "class": "", "width": ""},
    ]

    def get_h1(self):
        return f"Tickets Assigned to {self.request.user.first_name}"

    def get_queryset(self):
        return models.Ticket.objects.filter(dm_assigned=self.request.user.id).annotate(
            search_term=Concat('id', 'title', 'description', 'notes', output_field=TextField()))

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {"status": 2, }
        return kwargs


class TicketDetailView(LoginRequiredMixin, CommonDetailView):
    model = models.Ticket
    home_url_name = "tickets:router"
    template_name = "tickets/ticket_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['email'] = emails.TicketResolvedEmail(self.object)
        context["field_group_1"] = [
            "primary_contact",
            "dm_assigned",
            "app_display|app",
            "section",
            "description_html|Description",
            "status",
            "priority",
            "request_type",
        ]

        context["field_group_2"] = [
            "github_issue_number",
            "financial_coding",
            "estimated_cost",
            "financial_follow_up_needed",
            "people_notes",
            "date_opened",
            "date_modified",
            "date_closed",
            "resolved_email_date",
        ]

        context["field_group_4"] = [
            "sd_ref_number",
            "sd_ticket_url",
            "sd_primary_contact",
            "sd_description_html|Service desk ticket description",
            "sd_date_logged",
        ]
        return context


def send_resolved_email(request, ticket):
    # grab a copy of the resource
    my_ticket = models.Ticket.objects.get(pk=ticket)
    # create a new email object
    email = emails.TicketResolvedEmail(my_ticket)
    # send the email object
    custom_send_mail(
        subject=email.subject,
        html_message=email.message,
        from_email=email.from_email,
        recipient_list=email.to_list
    )

    my_ticket.resolved_email_date = timezone.now()
    my_ticket.save()
    messages.success(request, "the email has been sent!")
    return HttpResponseRedirect(reverse('tickets:detail', kwargs={'pk': ticket}))


def mark_ticket_resolved(request, ticket):
    my_ticket = models.Ticket.objects.get(pk=ticket)
    my_ticket.status_id = 1
    my_ticket.save()

    # if there is a github issue number, we should also make sure the issue is resolved.
    if my_ticket.github_issue_number:
        my_response = resolve_github_issue(my_ticket, request.user)

    return HttpResponseRedirect(reverse('tickets:detail', kwargs={'pk': ticket}))


def mark_ticket_active(request, ticket):
    my_ticket = models.Ticket.objects.get(pk=ticket)
    my_ticket.status_id = 2
    my_ticket.date_closed = None
    my_ticket.save()

    if my_ticket.github_issue_number:
        reopen_github_issue(my_ticket, request.user)

    return HttpResponseRedirect(reverse('tickets:detail', kwargs={'pk': ticket}))


class TicketUpdateView(LoginRequiredMixin, CommonUpdateView):
    model = models.Ticket
    template_name = "tickets/ticket_form.html"

    form_class = forms.TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save()

        # nobody is assigned, assign everyone
        if self.object.dm_assigned.count() == 0:
            for u in User.objects.filter(is_superuser=True):
                self.object.dm_assigned.add(u)

        # if there is a github issue number, we should also make sure the ticket is up to date.
        if self.object.github_issue_number:
            edit_github_issue(self.object.id, self.request.user.id)

        return HttpResponseRedirect(self.get_success_url())


class TicketDeleteView(LoginRequiredMixin, CommonDeleteView):
    model = models.Ticket
    success_url = reverse_lazy('tickets:router')
    template_name = "tickets/confirm_delete.html"


class TicketCreateView(LoginRequiredMixin, CommonCreateView):
    model = models.Ticket
    form_class = forms.TicketForm
    template_name = 'tickets/ticket_form.html'
    home_url_name = "tickets:router"

    def get_initial(self):
        return {'primary_contact': self.request.user}

    def form_valid(self, form):
        self.object = form.save()

        # nobody is assigned, assign DJF
        if self.object.dm_assigned.count() == 0:
            for u in User.objects.filter(is_superuser=True):
                self.object.dm_assigned.add(u)

        # create a new email object
        email = emails.NewTicketEmail(self.object)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )
        messages.success(self.request, "The new ticket has been logged and a confirmation email has been sent!")

        # check to see if a generic file should be appended
        if form.cleaned_data["generic_file_to_load"]:
            return HttpResponseRedirect(reverse_lazy("tickets:add_generic_file",
                                                     kwargs={"ticket": self.object.id, "type": form.cleaned_data["generic_file_to_load"]}))

        # if nothing, just go to detail page
        else:
            return HttpResponseRedirect(self.get_success_url())


class TicketCreateViewPopout(LoginRequiredMixin, CommonPopoutCreateView):
    model = models.Ticket
    form_class = forms.FeedbackForm

    # template_name = "tickets/ticket_form_popout.html"

    def get_initial(self):
        my_dict = {
            'primary_contact': self.request.user,
            'request_type': 19,
        }
        try:
            self.kwargs['app']
        except KeyError:
            pass
        else:
            my_dict["app"] = self.kwargs['app']

        return my_dict

    def form_valid(self, form):
        self.object = form.save()

        # nobody is assigned, assign everyone
        if self.object.dm_assigned.count() == 0:
            for u in User.objects.filter(is_superuser=True):
                self.object.dm_assigned.add(u)

        # create a new email object
        email = emails.NewTicketEmail(self.object)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )
        return HttpResponseRedirect(reverse_lazy('tickets:confirm'))


class TicketConfirmationTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "tickets/ticket_confirmation.html"


class TicketNoteUpdateView(LoginRequiredMixin, CommonUpdateView):
    model = models.Ticket
    form_class = forms.TicketNoteForm
    template_name = 'tickets/form.html'
    home_url_name = "tickets:router"
    h1 = "Edit notes"

    def get_parent_crumb(self):
        return {"title":self.get_object(), "url": reverse("tickets:detail" , args=[self.get_object().id])}


# Files #
#########

class FileCreateView(LoginRequiredMixin, CommonPopoutCreateView):
    model = models.File
    is_multipart_form_data = True
    form_class = forms.FileForm

    def get_initial(self):
        ticket = models.Ticket.objects.get(pk=self.kwargs['ticket'])
        return {'ticket': ticket}

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewFileAddedEmail(self.object)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )

        return HttpResponseRedirect(reverse('shared_models:close_me'))


class FileUpdateView(LoginRequiredMixin, CommonPopoutUpdateView):
    model = models.File
    form_class = forms.FileForm
    template_name = 'tickets/file_form_popout.html'
    is_multipart_form_data = True


class FileDetailView(LoginRequiredMixin, CommonPopoutDetailView):
    model = models.File
    template_name = 'tickets/file_detail_popout.html'
    field_list = [
        'caption',
        "date_created",
        "file",
    ]


class FileDeleteView(LoginRequiredMixin, CommonPopoutDeleteView):
    model = models.File


def add_generic_file(request, ticket, type):
    if type == "monitor":
        filename = "5166_Hardware_Request_Monitor.pdf"
    elif type == "computer":
        filename = "5166_Hardware_Request_Computer.pdf"
    elif type == "software":
        filename = "5165_Software_Request.pdf"
    elif type == "security_exemption":
        filename = "Request_DFO_IT_Security_Exemption.doc"

    source_file = os.path.join(settings.STATIC_DIR, "docs", "dm_tickets", filename)
    target_dir = os.path.join(settings.MEDIA_DIR, "tickets", "ticket_{}".format(ticket))
    target_file = os.path.join(target_dir, filename)

    # create the new folder
    try:
        os.mkdir(target_dir)
    except:
        print("folder already exists")

    copyfile(source_file, target_file)

    my_new_file = models.File.objects.create(
        caption="unsigned {} request form".format(type),
        ticket_id=ticket,
        date_created=timezone.now(),
        file="tickets/ticket_{}/{}".format(ticket, filename)
    )

    return HttpResponseRedirect(reverse('tickets:detail', kwargs={'pk': ticket}))


# Follow ups #
##############

class FollowUpCreateView(LoginRequiredMixin, CommonPopoutCreateView):
    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_h3(self):
        ticket = models.Ticket.objects.get(pk=self.kwargs['ticket'])
        if ticket.github_issue_number and self.request.is_staff:
            return f'HEADS UP: this follow-up will be created as a github comment on issue { ticket.github_issue_number }'


    def get_initial(self):
        ticket = models.Ticket.objects.get(pk=self.kwargs['ticket'])
        return {
            'ticket': ticket,
            'created_by': self.request.user.id,
            'created_date': timezone.now()
        }

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewFollowUpEmail(self.object)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )

        # github
        if self.object.ticket.github_issue_number:
            # If a github issue number exists, create this follow up as a comment
            my_comment = create_or_edit_comment(
                self.object.created_by_id,
                self.object.message,
                self.object.ticket.github_issue_number,
            )
            self.object.github_id = my_comment.id
            self.object.save()
        return HttpResponseRedirect(reverse('shared_models:close_me'))


class FollowUpUpdateView(LoginRequiredMixin, CommonPopoutUpdateView):
    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_h3(self):
        if self.get_object().ticket.github_issue_number and self.request.is_staff:
            return f'HEADS UP: this follow-up will be updated as a github comment on issue { self.get_object().github_issue_number }'

    def get_initial(self):
        return {
            'created_by': self.request.user.id,
            'created_date': timezone.now()
        }

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewFollowUpEmail(self.object)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )

        # github
        if self.object.ticket.github_issue_number:
            # If a github issue number exists, create this follow up as a comment

            my_comment = create_or_edit_comment(
                self.object.created_by_id,
                self.object.message,
                self.object.ticket.github_issue_number,
                self.object.github_id,
            )
            self.object.github_id = my_comment.id
            self.object.save()
        return HttpResponseRedirect(reverse('shared_models:close_me'))


class FollowUpDeleteView(LoginRequiredMixin, CommonPopoutDeleteView):
    model = models.FollowUp

    def delete(self, request, *args, **kwargs):
        # If a github comment id exists, delete the comment on github as well
        my_followup = models.FollowUp.objects.get(pk=self.kwargs["pk"])
        if my_followup.github_id:
            delete_comment(
                my_followup.ticket.github_issue_number,
                my_followup.github_id,
            )
        return super().delete(request, *args, **kwargs)


# REPORTS #
###########

class FinanceReportListView(LoginRequiredMixin, FilterView):
    filterset_class = filters.FiscalFilter
    template_name = "tickets/finance_report.html"
    queryset = models.Ticket.objects.filter(financial_follow_up_needed=True).filter(sd_ref_number__isnull=False).order_by("-date_opened")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def finance_spreadsheet(request):
    file_url = reports.generate_finance_spreadsheet()

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename="data management report for finance.xlsx"'
            return response
    raise Http404


# GitHub Views #
################

def get_github_repo():
    g = Github(settings.GITHUB_API_KEY)
    repo = g.get_repo("dfo-mar-odis/dm_apps")
    return repo


def create_github_issue(request, pk):
    my_ticket = models.Ticket.objects.get(pk=pk)
    my_user = request.user
    my_repo = get_github_repo()
    descr = "{} _[Added to GitHub by {} {}. Ticket created in DM Tickets by {} {}. Full ticket available [here](http://dmapps{}).]_".format(
        my_ticket.description,
        my_user.first_name,
        my_user.last_name,
        my_ticket.primary_contact.first_name,
        my_ticket.primary_contact.last_name,
        reverse("tickets:detail", kwargs={"pk": pk})
    )

    my_issue = my_repo.create_issue(
        title=my_ticket.title,
        body=descr,
        labels=[my_ticket.app, my_ticket.request_type.request_type],
    )
    my_ticket.github_issue_number = my_issue.number
    my_ticket.save()

    # if the ticket has some existing followups, they should be added as comments.
    if my_ticket.follow_ups.count() > 0:
        for f in my_ticket.follow_ups.all():
            create_or_edit_comment(my_user.id, f.message, my_issue.number)

    return HttpResponseRedirect(reverse("tickets:detail", kwargs={"pk": pk}))


def resolve_github_issue(ticket_object, user_object):
    """ This should only be called from within a view. This function does not return an HTTP response. Returns instance of github comment """

    my_repo = get_github_repo()
    my_issue = my_repo.get_issue(
        number=ticket_object.github_issue_number
    )
    my_issue.edit(state="closed")
    my_issue.create_comment("Closed by {} {} through DM Tickets".format(
        user_object.first_name,
        user_object.last_name,
    ))

    # ticket_object.github_resolved = True
    # ticket_object.save()

    return None


def reopen_github_issue(ticket_object, user_object):
    """ This should only be called from within a view. This function does not return an HTTP response. Returns instance of github comment """

    my_repo = get_github_repo()
    my_issue = my_repo.get_issue(
        number=ticket_object.github_issue_number
    )
    my_issue.edit(state="open")
    my_issue.create_comment("Re-opened by {} {} through DM Tickets".format(
        user_object.first_name,
        user_object.last_name,
    ))
    # ticket_object.github_resolved = False
    # ticket_object.save()
    return None


def create_or_edit_comment(user, message, issue_number, comment_id=None):
    """ This should only be called from within a view. This function does not return an HTTP response. Returns instance of github comment """
    my_user = User.objects.get(pk=user)
    my_repo = get_github_repo()
    my_issue = my_repo.get_issue(
        number=issue_number
    )

    # if a comment_id was provided, then go ahead an recall that object
    if comment_id:
        my_comment = my_issue.get_comment(comment_id)
        my_comment.edit(body=message)
    else:
        message = "{} _[created by {} {} through DM Tickets]_".format(
            message,
            my_user.first_name,
            my_user.last_name,
        )
        my_comment = my_issue.create_comment(message)

    return my_comment


def delete_comment(issue_number, comment_id):
    """ This should only be called from within a view. This function does not return an HTTP response. Returns None object """
    my_repo = get_github_repo()
    my_issue = my_repo.get_issue(
        number=issue_number
    )
    my_comment = my_issue.get_comment(comment_id)
    my_comment.delete()

    return None


def edit_github_issue(ticket, user):
    """ This should only be called from within a view. This function does not return an HTTP response. Returns None object """
    my_ticket = models.Ticket.objects.get(pk=ticket)
    my_user = User.objects.get(pk=user)
    my_repo = get_github_repo()
    descr = "{} _[Added to GitHub by {} {}. Ticket created in DM Tickets by {} {}. Full ticket available [here](http://dmapps{}).]_".format(
        my_ticket.description,
        my_user.first_name,
        my_user.last_name,
        my_ticket.primary_contact.first_name,
        my_ticket.primary_contact.last_name,
        reverse("tickets:detail", kwargs={"pk": ticket})
    )
    my_issue = my_repo.get_issue(
        number=my_ticket.github_issue_number,
    )
    my_issue.edit(
        title=my_ticket.title,
        body=descr,
        labels=[my_ticket.app, my_ticket.request_type.request_type],
    )

    return None
