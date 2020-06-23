from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate

from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest as CommonTest
from .. import views
