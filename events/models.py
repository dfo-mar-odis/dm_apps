from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, pluralize
from django.utils.translation import gettext_lazy as _, gettext

from masterlist.models import Person
from shared_models.models import SimpleLookup, Lookup, HelpTextLookup, FiscalYear, Language
from shared_models.utils import get_metadata_string


class Event(SimpleLookup):
    type_choices = (
        (1, _("CSAS Regional Advisory Process (RAP)")),
        (2, _("CSAS Science Management Meeting")),
        (3, _("CSAS Steering Committee Meeting")),
        (9, _("other")),
    )

    # basic
    location = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("location"))
    proponent = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("proponent"))
    type = models.IntegerField(choices=type_choices, verbose_name=_("type of event"))
    start_date = models.DateTimeField(verbose_name=_("initial activity date"), blank=True, null=True)
    end_date = models.DateTimeField(verbose_name=_("anticipated end date"), blank=True, null=True)
    from_email = models.EmailField(default=settings.SITE_FROM_EMAIL, verbose_name=_("FROM email address (on invitation)"))
    rsvp_email = models.EmailField(verbose_name=_("RSVP email address (on invitation)"))

    # calculated
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("fiscal year"), related_name="events",
                                    editable=False)
    # meta
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date last modified"), editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("last modified by"), editable=False,
                                   related_name="user_events_updated_by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"), editable=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("created by"), related_name="user_events_created_by",
                                   editable=False)
    parent_event = models.ForeignKey("Event", related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("parent event"))

    @property
    def metadata(self):
        return get_metadata_string(
            self.created_at,
            self.created_by,
            self.updated_at,
            self.updated_by,
        )

    class Meta:
        ordering = ['-updated_at', ]

    @property
    def attendees(self):
        return Attendance.objects.filter(invitee__event=self).order_by("invitee").values("invitee").distinct()

    @property
    def length_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1

    @property
    def display_dates(self):
        start = date(self.start_date) if self.start_date else "??"
        dates = f'{start}'
        if self.end_date and self.end_date != self.start_date:
            end = date(self.end_date)
            dates += f' &rarr; {end}'
        days_display = "{} {}{}".format(self.length_days, gettext("day"), pluralize(self.length_days))
        dates += f' ({days_display})'
        return dates


class Invitee(models.Model):
    # Choices for role
    role_choices = (
        (1, 'Participant'),
        (2, 'Chair'),
        (3, 'Expert'),
        (4, 'Steering Committee Member'),
    )
    status_choices = (
        (0, 'Invited'),
        (1, 'Accepted'),
        (2, 'Declined'),
        (9, 'No response'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invitees")

    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"), blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone"))
    email = models.EmailField(verbose_name=_("email"))
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("language preference"))

    role = models.IntegerField(choices=role_choices, verbose_name=_("Function"), default=1)
    organization = models.CharField(max_length=50, verbose_name=_("Association"), blank=True, null=True)
    status = models.IntegerField(choices=status_choices, verbose_name=_("status"), default=0)
    invitation_sent_date = models.DateTimeField(verbose_name=_("date invitation was sent"), editable=False, blank=True, null=True)
    resources_received = models.ManyToManyField("Resource", editable=False)

    class Meta:
        ordering = ['first_name', "last_name"]
        unique_together = (("event", "email"),)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def attendance_fraction(self):
        return self.attendance.count() / self.event.length_days


class Attendance(models.Model):
    invitee = models.ForeignKey(Invitee, on_delete=models.CASCADE, related_name="attendance", verbose_name=_("attendee"))
    date = models.DateTimeField(verbose_name=_("date"))

    class Meta:
        ordering = ['date']
        unique_together = (("invitee", "date"),)


class Note(models.Model):
    # Choices for type
    type_choices = (
        (1, 'To Do'),
        (2, 'Next step'),
        (3, 'General comment'),
    )

    event = models.ForeignKey(Event, related_name='notes', on_delete=models.CASCADE)
    type = models.IntegerField(choices=type_choices, verbose_name=_("type"))
    note = models.TextField(verbose_name=_("note"))
    is_complete = models.BooleanField(default=False, verbose_name=_("complete?"))

    # meta
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date last modified"), editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("last modified by"), editable=False,
                                   related_name="user_event_notes_updated_by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"), editable=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("created by"), editable=False,
                                   related_name="user_event_notes_created_by")

    @property
    def metadata(self):
        return get_metadata_string(
            self.created_at,
            self.created_by,
            self.updated_at,
            self.updated_by,
        )

    class Meta:
        ordering = ["is_complete", "-updated_at", ]


def resource_directory_path(instance, filename):
    return 'events/{0}/{1}'.format(instance.event.id, filename)


class Resource(SimpleLookup):
    event = models.ForeignKey(Event, related_name='resources', on_delete=models.CASCADE)

    url_en = models.URLField(verbose_name=_("url (English)"), blank=True, null=True)
    url_fr = models.URLField(verbose_name=_("url (French)"), blank=True, null=True)
    # file_en = models.FileField(upload_to=resource_directory_path, verbose_name=_("file attachment (English)"), blank=True, null=True)
    # file_fr = models.FileField(upload_to=resource_directory_path, verbose_name=_("file attachment (French)"), blank=True, null=True)

    # meta
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date last modified"), editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("last modified by"), editable=False,
                                   related_name="user_event_resources_updated_by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"), editable=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_("created by"), related_name="user_event_resources_created_by",
                                   editable=False)

    @property
    def metadata(self):
        return get_metadata_string(
            self.created_at,
            self.created_by,
            self.updated_at,
            self.updated_by,
        )

    @property
    def tfile(self):
        # check to see if a french value is given
        if getattr(self, gettext("file_en")):
            return getattr(self, gettext("file_en"))
        # if there is no translated term, just pull from the english field
        else:
            return self.file_en

    @property
    def turl(self):
        # check to see if a french value is given
        if getattr(self, gettext("url_en")):
            return getattr(self, gettext("url_en"))
        # if there is no translated term, just pull from the english field
        else:
            return self.url_en

    class Meta:
        ordering = [_("name")]
