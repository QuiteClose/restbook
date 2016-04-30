
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from . import controller

###############################################################################

class _AbstractControllerTest:
    '''
    Abstract testcase for any controller based tests.
    '''

    def setUp(self):
        self.controller = controller


###############################################################################

class ControllerFunctionalTest(_AbstractControllerTest, TestCase):
    '''
    Functional tests for a controller module.
    '''

    @given(name=text(), description=text())
    def test_can_store_restaurants(self, name, description):
        '''
        We should be able to create restaurants, save them and then
        retreive them afterwards.
        '''

        unique_id = self.controller.restaurant_create(
            name=name,
            description=description,
            opening_times=None,
            tables=None
        )

        assert(unique_id is not None)


###############################################################################

class ControllerUnitTest(_AbstractControllerTest, TestCase):
    '''
    Unit tests for the controller module
    '''

    def test_has_expected_attributes(self):
        feeback = 'Controller module "{module}" should have attribute "{attr}"'
        expected = (
            'restaurant_create',
        )

        for attribute in expected:
            self.assertTrue(
                hasattr(self.controller, attribute),
                feeback.format(module=self.controller.__name__, attr=attribute)
            )

