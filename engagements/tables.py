import django_tables2 as tables

from .models import Organization, Individual, EngagementPlan, Interaction

TABLE_ATTRIBUTE = {"class": 'table table-hover'}  # Bootstrap class
TABLE_TEMPLATE = "engagements/table_object_list.html"  # Modified included BS4 template


class OrganizationListTable(tables.Table):
    legal_name = tables.Column(accessor='legal_name', verbose_name='Name', order_by=('legal_name'), linkify=True)
    location = tables.Column(accessor='location_long', verbose_name='Location',
                             order_by=('country', 'province', 'city'))

    class Meta:
        model = Organization
        fields = ('legal_name', 'phone_number', 'location', 'stakeholder_type')
        attrs = TABLE_ATTRIBUTE
        template_name = TABLE_TEMPLATE


class IndividualListTable(tables.Table):
    full_name = tables.Column(accessor='full_name', verbose_name='Name', order_by=('last_name', 'first_name'),
                              linkify=True)

    class Meta:
        model = Individual
        fields = ('full_name', 'organization', 'title', 'email_address', 'phone_number',)
        attrs = TABLE_ATTRIBUTE
        template_name = TABLE_TEMPLATE


class PlanListTable(tables.Table):
    title = tables.Column(accessor='title', verbose_name='Title', order_by=('title'), linkify=True)

    class Meta:
        model = EngagementPlan
        fields = ('title', 'lead', 'region', 'status')
        attrs = TABLE_ATTRIBUTE
        template_name = TABLE_TEMPLATE


class InteractionListTable(tables.Table):
    title = tables.Column(accessor='title', verbose_name='Title', order_by=('title'), linkify=True)

    class Meta:
        model = Interaction
        fields = ('title', 'activity_type', 'organization_attendees', 'engagement_plan', 'date')
        attrs = TABLE_ATTRIBUTE
        template_name = TABLE_TEMPLATE
