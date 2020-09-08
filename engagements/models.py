from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from shared_models.models import Province, Region

ORGANIZATION_TYPES = [
    ('', '----'),
    ('Federal Government', 'Federal Government'),
    ('Provincial/State Government', 'Provincial/State Government'),
    ('Municipal Government', 'Municipal Government'),
    ('Indigenous Group/Government', 'Indigenous Group/Government'),
    ('Association', 'Association'),
    ('Small and Medium-Sized Business', 'Small and Medium-Sized Business'),
    ('Multinational Enterprise', 'Multinational Enterprise'),
    ('Accelerator/Incubator/Network', 'Accelerator/Incubator/Network'),
    ('PSI', 'Post-Secondary Institution'),
    ('Other', 'Other')
]

PROFIT_OPTIONS = [
    (None, '----'),
    (1, 'Profit'),
    (0, 'Non-Profit')
]

STAKEHOLDER_TYPE = [
    (1, 'Internal'),
    (2, 'Government of Canada'),
    (3, 'External')
]

PLANNED_STRING = 'Planned/Not Started'
STATUS = [
    (PLANNED_STRING, PLANNED_STRING),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('On Hold/Deferred', 'On Hold/Deferred'),
    ('Cancelled', 'Cancelled')
]

ACTIVITY_TYPE = [
    ('Phone', 'Phone'),
    ('Email', 'Email'),
    ('Meeting', 'Meeting'),
    ('Letter', 'Letter'),
    ('Conference', 'Conference'),
    ('Round-table', 'Round-table'),
    ('Announcement', 'Announcement'),
    ('Briefing', 'Briefing'),
    ('Workshop', 'Workshop'),
    ('Videoconference/Online', 'Videoconference/Online')
]

INITIATOR = [
    ('Staff', 'Staff'),
    ('Stakeholder', 'Stakeholder')
]

PRIORITY = [
    (1, 'Urgent'),
    (2, 'High'),
    (3, 'Normal'),
    (4, 'Low')
]

SUBJECTS = [
    ('Fisheries Act Changes', 'Fisheries Act Changes'),
    ('Indigenous Consultation', 'Indigenous Consultation'),
    ('Indigenous Knowledge', 'Indigenous Knowledge'),
    ('Codes of Practice', 'Codes of Practice'),
    ('Prescribed Works and Water Regulation', 'Prescribed Works and Water Regulation'),
    ('Engagement Framework and Tracking', 'Engagement Framework and Tracking'),
    ('Public Registry', 'Public Registry'),
    ('Offsetting and Banking', 'Offsetting and Banking'),
    ('Risk Management Approach', 'Risk Management Approach'),
    ('Death of Fish', 'Death of Fish'),
    ('Cumulative Effects', 'Cumulative Effects'),
    ('Marine Response Recovery Process', 'Marine Response Recovery Process')
]

OBJECTIVES = [
    ('Consultation', 'Consultation'),
    ('Convening', 'Convening'),
    ('Disseminate information', 'Disseminate information'),
    ('Establish/maintain partnerships', 'Establish/maintain partnerships'),
    ('Establish/maintain relationships', 'Establish/maintain relationships'),
    ('Gather intelligence', 'Gather intelligence'),
    ('Professional development', 'Professional development'),
    ('Program development', 'Program development'),
]

GEO_LEVEL = [
    (1, 'Regional'),
    (2, 'National'),
    (3, 'International')
]


class Organization(models.Model):
    legal_name = models.CharField(max_length=127)
    phone_number = PhoneNumberField(blank=True)
    fax_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    webpage = models.URLField(blank=True)
    business_number = models.CharField('CRA Business Number', max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=31, blank=True)
    address_line_2 = models.CharField(max_length=31, blank=True)
    city = models.CharField(max_length=15, blank=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING, blank=True, related_name='organizations',
                                 null=True)
    zip_postal = models.CharField("ZIP/Postal Code", max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True, default='Canada')
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES, default='', blank=True)
    other_organization_type = models.CharField(max_length=50, blank=True)  # Show if organization_type == 'Other'
    profit_nonprofit = models.PositiveIntegerField('Profit/Non-Profit', choices=PROFIT_OPTIONS, default=None,
                                                   blank=True, null=True)
    stakeholder_type = models.PositiveIntegerField(choices=STAKEHOLDER_TYPE, default=3)
    parent_organizations = models.ManyToManyField('self', symmetrical=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_organizations')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modified_organizations')
    slug = models.SlugField(max_length=127)

    def __str__(self):
        return self.legal_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.__str__())
        super(Organization, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('engagements:organization_detail', kwargs={'slug': self.slug})

    @property
    def stakeholder_type_str(self):
        type_str = [item[1] for item in STAKEHOLDER_TYPE if item[0] == self.stakeholder_type]
        return str(type_str[0])

    @property
    def profit_str(self):
        type_str = [item[1] for item in PROFIT_OPTIONS if item[0] == self.profit_nonprofit]
        return str(type_str[0])

    @property
    def location_long(self):
        out = ""
        if self.city is not None:
            out += f"{self.city}"

        if self.province is not None:
            if self.province.abbrev_eng is not None:
                if out == "":
                    out += self.province.abbrev_eng
                else:
                    out += f", {self.province.abbrev_eng}"
            else:
                if out == "":
                    out += self.province.name
                else:
                    out += f", {self.province.name}"

        else:
            if self.country is not None:
                if out == "":
                    out += self.country
                else:
                    out += f", {self.country}"

        return out


class Individual(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    title = models.CharField(max_length=45, blank=True)
    organization = models.ManyToManyField(Organization, blank=True)
    email_address = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    fax_number = PhoneNumberField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=31, blank=True)
    address_line_2 = models.CharField(max_length=31, blank=True)
    city = models.CharField(max_length=15, blank=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING, blank=True, related_name='individuals',
                                 null=True)
    zip_postal = models.CharField("ZIP/Postal Code", max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True, default='Canada')
    linkedin_profile = models.URLField("LinkedIn profile", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_individuals')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modified_individuals')
    slug = models.SlugField(max_length=127)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.__str__())
        super(Individual, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('engagements:individual_detail', kwargs={'slug': self.slug})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class EngagementPlan(models.Model):
    title = models.CharField(max_length=250)
    lead = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                             related_name='engagement_plan_leads')
    region = models.ForeignKey(Region, models.DO_NOTHING, related_name='engagement_plans')
    summary = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    stakeholders = models.ManyToManyField(Organization, blank=True)
    staff_collaborators = models.ManyToManyField(User, blank=True, related_name='engagement_plan_collaborators')
    status = models.CharField(choices=STATUS, max_length=31, default=PLANNED_STRING)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_engagement_plan')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modified_engagement_plan')
    slug = models.SlugField(max_length=127)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.__str__())
        super(EngagementPlan, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('engagements:plan_detail', kwargs={'slug': self.slug})


class InteractionSubject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class InteractionObjective(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    activity_type = models.CharField(choices=ACTIVITY_TYPE, max_length=22)
    title = models.CharField(max_length=250)
    file_reference = models.CharField(max_length=31, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    engagement_plan = models.ForeignKey(EngagementPlan, models.SET_NULL, blank=True, null=True)
    initiator = models.CharField(choices=INITIATOR, max_length=11, default='Staff')
    primary_contact = models.ForeignKey(Individual, models.DO_NOTHING, related_name='interaction_primaries')
    staff_lead = models.ForeignKey(User, models.DO_NOTHING, related_name='interaction_leads')
    attendees = models.ManyToManyField(Individual, related_name='attended_interactions')
    organization_attendees = models.ManyToManyField(Organization, related_name='attended_interactions', blank=True)
    staff_attendees = models.ManyToManyField(User, related_name='attended_interactions')
    location = models.CharField(max_length=127, blank=True)
    status = models.CharField(choices=STATUS, max_length=31, default=PLANNED_STRING)
    priority = models.PositiveIntegerField(choices=PRIORITY, default=3)
    subjects = models.ManyToManyField(InteractionSubject, related_name='interaction_subjects')
    objectives = models.ManyToManyField(InteractionObjective, related_name='interaction_objectives')
    geographic_level = models.PositiveIntegerField(choices=GEO_LEVEL, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_interactions')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='modified_interactions')
    slug = models.SlugField(max_length=127)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.__str__())
        super(Interaction, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('engagements:interaction_detail', kwargs={'slug': self.slug})

    @property
    def priority_str(self):
        type_str = [item[1] for item in PRIORITY if item[0] == self.priority]
        return str(type_str[0])

    @property
    def geographic_level_str(self):
        type_str = [item[1] for item in GEO_LEVEL if item[0] == self.geographic_level]
        return str(type_str[0])
