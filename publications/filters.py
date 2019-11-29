import django_filters
from django_filters import FilterSet
from publications import models
import datetime


class ProjectFilter(FilterSet):

    class Meta:
        model = models.Project
        fields = [
            'title', 'theme', 'program_linkage', 'ecosystem_component', 'geographic_scope']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters['title'].lookup_expr = 'icontains'
        self.filters['theme'].conjoined = True
        self.filters['program_linkage'].conjoined = True
