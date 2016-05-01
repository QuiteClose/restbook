
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from restbook import entities

###############################################################################

class RestaurantUnitTest(TestCase):
    '''
    Unit tests for the Restaurant Entity
    '''

    @given(text(), text(), text(), text())
    def test_restaurant_init(self, name, description, opening_times, tables):
        '''
        The Restaurant.__init__ method should assign the given
        arguments to the correct properties.
        '''

        restaurant = entities.Restaurant(
            name=name,
            description=description,
            opening_times=opening_times,
            tables=tables
        )

        assert(name == restaurant.name)
        assert(description == restaurant.description)
        assert(opening_times == restaurant.opening_times)
        assert(tables == restaurant.tables)

##############################

    @given(text(), text())
    def test_restaurant_is_valid(self, name, description):
        '''
        Any restaurant with a name and a description should be valid.
        '''

        restaurant = entities.Restaurant(name=name, description=description)
        assert(restaurant.is_valid())

##############################

    def test_restaurants_must_have_a_name(self):
        '''
        Any restaurant without a name must fail validation.
        '''

        self.assertFalse(
            entities.Restaurant(name=None).is_valid(),
            'Restaurant names cannot be None.'
        )

        self.assertFalse(
            entities.Restaurant(name='').is_valid(),
            "Restaurant names cannot be ''."
        )

