
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from . import controller

###############################################################################

class ControllerTest(TestCase):
    '''
    Functioinal tests for a controller module.
    '''

    def setUp(self):
        self.controller = controller

##############################

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


