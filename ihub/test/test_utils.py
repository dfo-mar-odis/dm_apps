from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from shared_models.test.SharedModelsFactoryFloor import UserFactory
from ihub.test import FactoryFloor
from ihub.test.common_tests import CommonInventoryTest
