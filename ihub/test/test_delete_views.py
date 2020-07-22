from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DeleteView

from .. import models
from .. import views
from ihub.test.common_tests import CommonInventoryTest as CommonTest
from ihub.test import FactoryFloor

