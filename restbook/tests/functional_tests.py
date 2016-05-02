
from unittest import TestCase

from hypothesis import assume, given
from hypothesis.strategies import integers, lists, text

from restbook import controller
from restbook.tests import strategies

###############################################################################

class ControllerFunctionalTest(TestCase):
    '''
    Functional tests for a controller module.
    '''

    def setUp(self):
        self.controller = controller

##############################

    @given(
        name=text(),
        description=text(),
        opening_times=strategies.opening_times,
        tables=lists(integers(min_value=1, max_value=12))
    )
    def test_can_store_restaurants_with_opening_times(
        self,
        name,
        description,
        opening_times,
        tables
    ):
        '''
        We should be able to create and retreive restaurants.
        '''

        assume(name != '')

        unique_id = self.controller.restaurant_create(
            name=name,
            description=description,
            opening_times=opening_times,
            tables=tables
        )

        assert(unique_id is not None)

        restaurant = self.controller.restaurant_from_id(unique_id)

        assert(restaurant.name == name)
        assert(restaurant.description == description)
        assert(list(restaurant.opening_times) == list(opening_times))
        assert(list(restaurant.tables) == list(tables))

