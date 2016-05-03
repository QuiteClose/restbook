
import datetime
from unittest import TestCase

from hypothesis import assume, given
from hypothesis.extra.datetime import datetimes
from hypothesis.strategies import integers, lists, text, tuples

from restbook import entities, time
from restbook.tests import strategies

###############################################################################

class RestaurantUnitTest(TestCase):
    '''
    Unit tests for the Restaurant Entity
    '''

    @given(
        name=text(),
        description=text(),
        opening_times=strategies.opening_times,
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

##############################

    @given(
        name=text(),
        description=text(),
        tables=lists(integers()),
        times=strategies.opening_times_strings
    )
    def test_restaurant__str__(
        self,
        name,
        description,
        tables,
        times
    ):
        '''
        String representations of restaurants should include their name,
        description, opening times and tables.
        '''

        restaurant = entities.Restaurant(
            name=name,
            description=description,
            tables=tables,
            opening_times=times
        )

        string = str(restaurant)

        assert(name in string)
        assert(description in string)

        for n in range(len(tables)):
            table_details = '{table_number}: {table_size}'.format(
                table_number = n,
                table_size = tables[n]
            )
            assert(table_details in string)

        for open, close in times:
            period = '{open}-{close}'.format(open=open, close=close)
            assert(period in string)


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

    @given(times=strategies.opening_times_strings)
    def test_opening_times_may_be_tuples_of_strings(self, times):
        '''
        OpeningTimes should convert strings into MinuteOffset integers.
        '''

        try:
            opening_times = entities.OpeningTimes(times)
            entities.OpeningTimes.validate(opening_times)
        except ValueError:
            self.fail(
                'Opening times should be definable in terms of '
                'a list of tuples as of a pair of strings.'
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

class BookingUnitTest(TestCase):
    '''Test booking creation functionality.'''

##############################

    @given(
        reference=text(),
        covers=integers(min_value=1),
        start=datetimes(),
        finish=datetimes()
    )
    def test_booking_can_be_created(self, reference, covers, start, finish):
        '''
        Tests that bookings can be created using just a booking
        reference, the number of guests (covers) and a start and
        end-time.
        '''

        assume(start < finish)

        booking = entities.Booking(
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        assert(booking.is_valid())

##############################

    @given(
        reference=text(),
        covers=integers(min_value=1),
        start=datetimes(),
        finish=datetimes()
    )
    def test_booking_invalid_if_start_after_finish(
        self,
        reference,
        covers,
        start,
        finish
    ):
        '''
        A booking is invalid if it starts after it ends.
        '''

        assume(start > finish)

        booking = entities.Booking(
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        assert(not booking.is_valid())

##############################

    def test_booking_is_valid_represents_validate(self):
        '''
        Booking.is_valid should corresponds to Booking.validate
        according to any ValueError raised.
        '''

        def always_ValueError(a, b): raise ValueError;
        def never_ValueError(a, b): pass;

        booking = entities.Booking(
            reference='Safe Example',
            covers=1,
            start=datetime.datetime.now(),
            finish=datetime.datetime.now()
        )

        stash = entities.Booking.validate

        try:
            entities.Booking.validate = always_ValueError
            self.assertFalse(
                booking.is_valid(),
                'If Booking.validate raises a ValueError '
                'booking.is_valid should return False.'
            )

            entities.Booking.validate = never_ValueError
            self.assertTrue(
                booking.is_valid(),
                'If Booking.validate does not raise a ValueError '
                'booking.is_valid should return True.'
            )
        except ValueError:
            self.fail(
                'If Booking.validate raises a ValueError '
                'it should be caught by Booking.is_valid.'
            )
        finally:
            entities.Booking.validate = stash

##############################

    @given(
        context=datetimes()
    )
    def test_booking_within_times(self, context):
        '''
        Bookings.within should return false if it falls out-of-bounds.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = time.get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        bookings = [
            entities.Booking(
                reference='starts_too_soon',
                covers=1,
                start=datetime.datetime(year, month, day, 11, 0),
                finish=datetime.datetime(year, month, day, 13, 0),
            ),
            entities.Booking(
                reference='discarded_starts_too_late',
                covers=1,
                start=datetime.datetime(year, month, day, 14, 30),
                finish=datetime.datetime(year, month, day, 15, 0),
            ),
            entities.Booking(
                reference='discarded_finishes_too_late',
                covers=1,
                start=datetime.datetime(year, month, day, 13, 30),
                finish=datetime.datetime(year, month, day, 15, 0),
            ),
            entities.Booking(
                reference='kept',
                covers=1,
                start=datetime.datetime(year, month, day, 12, 0),
                finish=datetime.datetime(year, month, day, 14, 0),
            ),
        ]
        

        self.assertListEqual(
            [x for x in bookings if x.reference == 'kept'],
            [x for x in bookings if x.within(context, start, end)],
            'Bookings.within should be False if a booking is not within time.'
        )

##############################

    @given(
        context=datetimes()
    )
    def test_booking_within_times(self, context):
        '''
        Bookings.overlaps should determine whether two bookings overlap.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = time.get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        before = entities.Booking(
            reference='control',
            covers=1,
            start=datetime.datetime(year, month, day, 10, 0),
            finish=datetime.datetime(year, month, day, 13, 0),
        )

        after = entities.Booking(
            reference='Does not clash with booking',
            covers=1,
            start=datetime.datetime(year, month, day, 13, 0),
            finish=datetime.datetime(year, month, day, 16, 0),
        )

        both_clash = entities.Booking(
            reference='Clashes with both bookings',
            covers=1,
            start=datetime.datetime(year, month, day, 12, 0),
            finish=datetime.datetime(year, month, day, 14, 0),
        )

        self.assertFalse(
            before.overlaps(after),
            'Bookings.overlap should return False if two bookings do not clash.'
        )

        self.assertFalse(
            after.overlaps(before),
            'Bookings.overlap should return False if two bookings do not clash.'
        )

        self.assertTrue(
            before.overlaps(both_clash),
            'Bookings.overlap should return True if two bookings clash.'
        )

        self.assertTrue(
            after.overlaps(both_clash),
            'Bookings.overlap should return True if two bookings clash.'
        )

        self.assertTrue(
            both_clash.overlaps(before),
            'Bookings.overlap should return True if two bookings clash.'
        )

        self.assertTrue(
            both_clash.overlaps(after),
            'Bookings.overlap should return True if two bookings clash.'
        )
