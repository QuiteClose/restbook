
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import integers, lists, text, tuples

from restbook import entities
from restbook.tests import strategies

###############################################################################

class RestaurantUnitTest(TestCase):
    '''
    Unit tests for the Restaurant Entity
    '''

    @given(
        name=text(),
        description=text(),
        opening_times=lists(text()),
        tables=lists(integers())
    )
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
        assert(list(opening_times) == list(restaurant.opening_times))
        assert(list(tables) == list(restaurant.tables))

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

##############################

    @given(times=strategies.opening_times)
    def test_create_restaurants_with_opening_times(self, times):
        '''
        We should be able to create restaurants with opening times.
        '''

        restaurant = entities.Restaurant(
            name='Safe Example',
            opening_times=times
        )

        if not restaurant.is_valid():
            self.fail('Restaurant should validate with opening times.')

        if len(restaurant.opening_times) != len(times):
            self.fail('Restaurants should store all given opening times.')

##############################

    def test_restaurants_should_include_opening_times_in_validation(self):
        '''
        Restaurant validation should validate opening times.
        '''

        valid_times = entities.OpeningTimes([(0, 1)])
        invalid_times = entities.OpeningTimes([(2, 1)])

        restaurant = entities.Restaurant(name='Safe Example')

        restaurant.opening_times = valid_times
        self.assertTrue(
            restaurant.is_valid(),
            'Restaurants should validate with valid opening hours.'
        )

        restaurant.opening_times = invalid_times
        self.assertFalse(
            restaurant.is_valid(),
            'Restaurants should not validate with invalid opening hours.'
        )

##############################

    def test_restaurant_validation_should_fail_if_tables_are_not_ints(self):
        '''
        Tables should be a list of integers. Validation should fail otherwise.
        '''

        valid_restaurant = entities.Restaurant(
            name='Safe Example',
            tables=[1, 2, 3]
        )

        invalid_restaurant = entities.Restaurant(
            name='Safe Example',
            tables=[1, '2', 3]
        )

        self.assertTrue(
            valid_restaurant.is_valid(),
            'Restaurants should be valid '
            'if their tables are a list of integers.'
        )

        self.assertFalse(
            invalid_restaurant.is_valid(),
            'Restaurants should be invalid '
            'if their tables are not a list of integers.'
        )


##############################

    def test_restaurant_validation_should_fail_if_tables_are_not_positive(self):
        '''
        Tables should be a list of positive integers.
        Validation should fail otherwise.
        '''

        valid_restaurant = entities.Restaurant(
            name='Safe Example',
            tables=[1]
        )

        zero_restaurant = entities.Restaurant(
            name='Safe Example',
            tables=[0]
        )

        negative_restaurant = entities.Restaurant(
            name='Safe Example',
            tables=[-1]
        )

        self.assertTrue(
            valid_restaurant.is_valid(),
            'Restaurants should be valid '
            'if their tables are a list of positive integers.'
        )

        self.assertFalse(
            zero_restaurant.is_valid(),
            'Restaurants should be invalid '
            'if any of their tables are of zero size.'
        )

        self.assertFalse(
            negative_restaurant.is_valid(),
            'Restaurants should be invalid '
            'if any of their tables have a negative size.'
        )


###############################################################################

class OpeningTimesUnitTest(TestCase):
    '''
    Unit tests for the OpeningTimes Entity
    '''

    MINUTES_IN_WEEK = 10080

    @given(times=strategies.opening_times)
    def test_opening_times_may_be_tuples_of_integers(self, times):
        '''
        Uses the opening_times strategy to generate random valid
        opening times represented as a list of tuples. Each tuple should
        be a pair of integers representing start and end times as an
        offset from 0000 on Monday.
        '''

        try:
            opening_times = entities.OpeningTimes(times)
            entities.OpeningTimes.validate(opening_times)
        except ValueError:
            self.fail(
                'Opening times should be definable in terms of '
                'a list of tuples as of a pair of integers.'
            )

##############################

    def test_opening_times_should_start_after_0(self):
        '''
        The first start-time should be zero or greater.
        '''

        valid_times = entities.OpeningTimes([(0,1)])
        invalid_times = entities.OpeningTimes([(-1,1)])

        try:
            entities.OpeningTimes.validate(valid_times)
        except ValueError:
            self.fail(
                'Opening times are valid when the first start time is >= 0'
            )

        try:
            entities.OpeningTimes.validate(invalid_times)
        except ValueError:
            pass
        else:
            self.fail(
                'Opening times are invalid when the first start time is < 0'
            )

##############################

    def test_opening_times_should_start_before_end_of_week(self):
        '''
        The first start-time should be < minutes in week.
        '''

        valid_times = entities.OpeningTimes([
            (self.MINUTES_IN_WEEK, self.MINUTES_IN_WEEK)
        ])

        invalid_times = entities.OpeningTimes([
            (self.MINUTES_IN_WEEK+1, self.MINUTES_IN_WEEK+1)
        ])

        try:
            entities.OpeningTimes.validate(valid_times)
        except ValueError:
            self.fail(
                'Opening times are valid when they start before the end of the week.'
            )

        try:
            entities.OpeningTimes.validate(invalid_times)
        except ValueError:
            pass
        else:
            self.fail(
                'Opening times are invalid when they start after the end of the week.'
            )

##############################

    def test_opening_times_should_end_after_they_start(self):
        '''
        The start-time of a period should be <= the end-time.
        '''

        valid_times = entities.OpeningTimes([(0,1)])
        invalid_times = entities.OpeningTimes([(1,0)])

        try:
            entities.OpeningTimes.validate(valid_times)
        except ValueError:
            self.fail(
                'Opening times are valid when they end after they start.'
            )

        try:
            entities.OpeningTimes.validate(invalid_times)
        except ValueError:
            pass
        else:
            self.fail(
                'Opening times are invalid when they end before they start.'
            )


##############################

    def test_opening_times_should_not_overlap(self):
        '''
        The start-time of a period should be >= the previous end-time.
        '''

        valid_times = entities.OpeningTimes([(0,100), (100, 200)])
        invalid_times = entities.OpeningTimes([(0,100), (99, 200)])

        try:
            entities.OpeningTimes.validate(valid_times)
        except ValueError:
            self.fail(
                'Opening times are valid when they do not overlap.'
            )

        try:
            entities.OpeningTimes.validate(invalid_times)
        except ValueError:
            pass
        else:
            self.fail(
                'Opening times are invalid when they overlap.'
            )

##############################

    def test_last_opening_time_does_not_overlap_first(self):
        '''
        The last end-time should not overlap the first start-time.
        '''

        valid_times = entities.OpeningTimes([
            (0, 1),
            (self.MINUTES_IN_WEEK, self.MINUTES_IN_WEEK)
        ])

        invalid_times = entities.OpeningTimes([
            (0, 1),
            (self.MINUTES_IN_WEEK, self.MINUTES_IN_WEEK+1)
        ])

        try:
            entities.OpeningTimes.validate(valid_times)
        except ValueError:
            self.fail(
                'Opening times are valid when the last end-time '
                'does not overlap the first start-time.'
            )

        try:
            entities.OpeningTimes.validate(invalid_times)
        except ValueError:
            pass
        else:
            self.fail(
                'Opening times are invalid when the last end-time '
                'overlaps the first start-time.'
            )

##############################

    def test_is_valid_represents_validate(self):
        '''
        OpeningTimes.is_valid should correspond to OpeningTimes.validate
        according to any ValueError raised.
        '''

        def always_ValueError(a, b): raise ValueError;
        def never_ValueError(a, b): pass;

        opening_times = entities.OpeningTimes([(0,1)])
        stash = entities.OpeningTimes.validate

        try:
            entities.OpeningTimes.validate = always_ValueError
            self.assertFalse(
                opening_times.is_valid(),
                'If OpeningTimes.validate raises a ValueError '
                'OpeningTimes.is_valid should return False.'
            )

            entities.OpeningTimes.validate = never_ValueError
            self.assertTrue(
                opening_times.is_valid(),
                'If OpeningTimes.validate does not raise a ValueError '
                'restaurant.is_valid should return True.'
            )
        except ValueError:
            self.fail(
                'If OpeningTimes.validate raises a ValueError '
                'it should be caught by OpeningTimes.is_valid.'
            )
        finally:
            entities.OpeningTimes.validate = stash

###############################################################################

class MinuteOffsetUnitTest(TestCase):

    def test_minutes_in_week(self):
        '''
        Minutes in week must be accurate.
        '''

        self.assertEqual(
            entities.MinuteOffset.MINUTES_IN_WEEK,
            60 * 24 * 7,
            'Minutes in week must equal 60 * 24 * 7.'
        )

    def test_conversion_from_strings(self):
        '''
        Should convert from 'Monday 0000' to 0 or 'Monday 2000' to 1200.
        '''

        sample = (
            (0, 'Monday 00.00'),
            (61, 'Monday 01.01'),
            (1200, 'Monday 20.00'),
            (3480, 'Wednesday 10.00'),
            (5250, 'Thursday 15.30'),
            (7030, 'Friday 21.00'),
            (10079, 'Sunday 23.59'),
        )

        for example in sample:
            expected_result = example[0]
            given_string = example[1]

            self.assertEqual(
                expected_result,
                entities.MinuteOffset.from_string(given_string),
                'MinuteOffset.from_string should convert '
                '"{string}" to {offset}.'.format(string=given_string,
                                                 offset=expected_result)
            )

