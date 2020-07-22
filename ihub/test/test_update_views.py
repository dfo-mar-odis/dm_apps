from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import CreateView, UpdateView

from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonIHubTest as CommonTest
from .. import views
from .. import models

