from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView
from easy_pdf.views import PDFTemplateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views

