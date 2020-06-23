from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from shared_models.test.SharedModelsFactoryFloor import UserFactory
from inventory.test import FactoryFloor
from inventory.test.common_tests import CommonInventoryTest
