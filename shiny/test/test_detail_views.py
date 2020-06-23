from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView
from shiny.test import  FactoryFloor
from shiny.test.common_tests import CommonShinyTest as CommonTest
from .. import views
