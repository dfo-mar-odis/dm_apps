from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import ListView
from django_filters.views import FilterView
from .. import models
from .. import views

from ihub.test.common_tests import CommonInventoryTest as CommonTest
from ihub.test import FactoryFloor

