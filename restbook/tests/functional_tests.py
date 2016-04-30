
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from restbook import controller

###############################################################################

class ControllerFunctionalTest(TestCase):
    '''
    Functional tests for a controller module.
    '''

    def setUp(self):
        self.controller = controller

##############################

    @given(name=text(), description=text())
    def test_can_store_restaurants(self, name, description):
        '''
        We should be able to create and retreive restaurants.
        '''

        unique_id = self.controller.restaurant_create(
            name=name,
            description=description
        )

        assert(unique_id is not None)

        restaurant = self.controller.restaurant_from_id(unique_id)

        assert(restaurant.name == name)
        assert(restaurant.description == description)

