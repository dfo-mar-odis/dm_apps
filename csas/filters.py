import django_filters
# from django_filters import FilterSet
# from django import forms

from . import models


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = models.ConContact
        fields = ['last_name', 'first_name', 'contact_type', 'region', 'role', 'expertise']


class MeetingFilter(django_filters.FilterSet):
    start_date = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact')

    class Meta:
        model = models.MetMeeting
        fields = ['start_date', 'title_en', 'process_type', 'lead_region']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dates = [(y[0], str(y[0])) for y in models.MetMeeting.objects.all().values_list('start_date').distinct()]
        self.filters['start_date'] = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact', choices=dates)


class MeetingFilterDFOPars(django_filters.FilterSet):
    # meeting = django_filters.ChoiceFilter(field_name='meeting', lookup_expr='exact')

    class Meta:
        model = models.MetMeetingDFOPars
        fields = ['meeting', 'name', 'role', 'time']
        # fields = ['meeting', 'name', 'role', 'time', 'cost_category', 'funding_source', 'total_salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #meet = [(y[0], str(y[0])) for y in models.MetMeetingDFOPars.objects.all().values_list('meeting').distinct()]
        #self.filters['meeting'] = django_filters.ChoiceFilter(field_name='meeting', lookup_expr='exact', choices=meet)


class MeetingFilterOtherPars(django_filters.FilterSet):
    name = django_filters.ChoiceFilter(field_name='meeting', lookup_expr='exact')

    class Meta:
        model = models.MetMeetingOtherPars
        fields = ['meeting', 'name', 'role', 'affiliation', 'invited', 'attended']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dates = [(y[0], str(y[0])) for y in models.MetMeetingOtherPars.objects.all().values_list('meeting').distinct()]
        self.filters['meeting'] = django_filters.ChoiceFilter(field_name='meeting', lookup_expr='exact', choices=dates)


class PublicationFilter(django_filters.FilterSet):
    series = django_filters.CharFilter(field_name='series', lookup_expr='icontains')
    title_en = django_filters.CharFilter(field_name='title_en', lookup_expr='icontains')

    class Meta:
        model = models.PubPublication
        fields = ['series', 'title_en', 'lead_region', 'lead_author', 'other_author', 'pub_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dates = [(y[0], str(y[0])) for y in models.PubPublication.objects.all().values_list('pub_num').distinct()]
        # self.filters['pub_num'] = django_filters.ChoiceFilter(field_name='pub_num', lookup_expr='exact', choices=dates)


class RequestFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    client_name = django_filters.CharFilter(field_name='client_name', lookup_expr='icontains')

    class Meta:
        model = models.ReqRequest
        fields = ['title', 'region', 'client_sector', 'client_name', 'priority_id', 'funding']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dates = [(y[0], str(y[0])) for y in models.MetMeeting.objects.all().values_list('start_date').distinct()]
        # self.filters['start_date'] = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact', choices=dates)
