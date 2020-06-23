import django_filters
# from django_filters import FilterSet
# from django import forms

from . import models


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = models.ConContact
        fields = ['last_name', 'first_name', 'contact_type', 'region']


class MeetingFilter(django_filters.FilterSet):
    start_date = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact')

    class Meta:
        model = models.MetMeeting
        fields = ['start_date', 'title_en', 'process_type', 'lead_region']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dates = [(y[0], str(y[0])) for y in models.MetMeeting.objects.all().values_list('start_date').distinct()]
        self.filters['start_date'] = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact', choices=dates)


class PublicationFilter(django_filters.FilterSet):
    series = django_filters.CharFilter(field_name='series', lookup_expr='icontains')

    class Meta:
        model = models.PubPublication
        fields = ['series', 'lead_region', 'lead_author', 'pub_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dates = [(y[0], str(y[0])) for y in models.PubPublication.objects.all().values_list('pub_num').distinct()]
        # self.filters['pub_num'] = django_filters.ChoiceFilter(field_name='pub_num', lookup_expr='exact', choices=dates)


class RequestFilter(django_filters.FilterSet):
    # start_date = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact')
    region = django_filters.ChoiceFilter(field_name='region', lookup_expr='exact')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    client_name = django_filters.CharFilter(field_name='client_name', lookup_expr='icontains')

    class Meta:
        model = models.ReqRequest
        # fields = ['start_date', 'title_en', 'process_type', 'lead_region']
        fields = ['region', 'client_sector', 'title', 'client_name', 'funding']
        # fields = {'finding': ['Yes', 'No'],}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dates = [(y[0], str(y[0])) for y in models.MetMeeting.objects.all().values_list('start_date').distinct()]
        # self.filters['start_date'] = django_filters.ChoiceFilter(field_name='start_date', lookup_expr='exact', choices=dates)
