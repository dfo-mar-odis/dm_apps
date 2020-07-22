import datetime
from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from easy_pdf.views import PDFTemplateView
from faker import Faker

from lib.functions.custom_functions import fiscal_year
from shared_models.test.SharedModelsFactoryFloor import RegionFactory, UserFactory
from travel.test import FactoryFloor

from travel.test.common_tests import CommonTravelTest as CommonTest
from .FactoryFloor import ResourceFactory
from .. import views

faker = Faker()

