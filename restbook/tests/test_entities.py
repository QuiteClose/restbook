
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

    def test_restaurant_is_valid_represents_validate(self):
        '''
        Restaurant.is_valid should corresponds to Restaurant.validate
        according to any ValueError raised.
        '''

        def always_ValueError(a, b): raise ValueError;
        def never_ValueError(a, b): pass;

        restaurant = entities.Restaurant(name='Safe', description='Example')
        stash = entities.Restaurant.validate

        try:
            entities.Restaurant.validate = always_ValueError
            self.assertFalse(
                restaurant.is_valid(),
                'If Restaurant.validate raises a ValueError '
                'restaurant.is_valid should return False.'
            )

            entities.Restaurant.validate = never_ValueError
            self.assertTrue(
                restaurant.is_valid(),
                'If Restaurant.validate does not raise a ValueError '
                'restaurant.is_valid should return True.'
            )
        except ValueError:
            self.fail(
                'If Restaurant.validate raises a ValueError '
                'it should be caught by Restaurant.is_valid.'
            )
        finally:
            entities.Restaurant.validate = stash

##############################

    def test_restaurants_must_have_a_name(self):
        '''
        Any restaurant without a name must fail validation.
        '''

        no_name = entities.Restaurant(name=None)
        empty_name = entities.Restaurant(name='')

        try:
            entities.Restaurant.validate(no_name)
        except ValueError:
            pass
        else:
            self.fail(
                'When name is None Restaurant.validate should '
                'raise a ValueError.'
            )

        try:
            entities.Restaurant.validate(empty_name)
        except ValueError:
            pass
        else:
            self.fail(
                'When name is \'\' Restaurant.validate should '
                'raise a ValueError.'
            )


##############################

    def test_opening_times_must_be_iterable(self):
        '''
        We should be able to iterate over opening times.
        '''

        restaurant = entities.Restaurant(name='Safe', description='Example')

        self.assertIsNotNone(
            restaurant.opening_times.__iter__(),
            'A restaurants opening times should be iterable.'
        )
