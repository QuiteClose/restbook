
from datetime import datetime
from unittest import TestCase

from hypothesis import assume, given
from hypothesis.extra.datetime import datetimes
from hypothesis.strategies import integers, lists, text

from restbook import controller
from restbook.tests import strategies

###############################################################################

class RestaurantsFunctionalTest(TestCase):
    '''
    Functional tests for restuarants.
    '''

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

        unique_id = controller.restaurant_create(
            name=name,
            description=description,
            opening_times=opening_times,
            tables=tables
        )

        assert(unique_id is not None)

        restaurant = controller.restaurant_from_id(unique_id)

        assert(restaurant.name == name)
        assert(restaurant.description == description)
        assert(list(restaurant.opening_times) == list(opening_times))
        assert(list(restaurant.tables) == list(tables))

###############################################################################

class BookingsFunctionalTest(TestCase):
    '''
    We should be able to create bookings and access them afterwards.
    '''

    def test_can_make_a_booking_and_access_it(self):
        '''
        If a restaurant is open and has space we should be able to book 
        tables.
        '''

        reference='Successful'
        covers=1
        start=datetime(2016, 5, 2, 13, 0)  # Monday 13.00
        finish=datetime(2016, 5, 2, 15, 0) # Monday 15.00

        restaurant_id = controller.restaurant_create(
            name='Safe',
            description='Example',
            opening_times=[
                ('Monday 12.00', 'Monday 16.00'),
            ],
            tables=[1]
        )

        booking_id = controller.booking_create(
            restaurant_id=restaurant_id,
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        self.assertIsNotNone(
            booking_id,
            'We should be able to create a booking if the restaurant is open.'
        )

        booking = controller.booking_from_id(booking_id)

        assert(booking.reference == reference)
        assert(booking.covers == covers)
        assert(booking.start == start)
        assert(booking.finish == finish)

##############################

    def test_booking_fails_if_restaurant_is_closed(self):
        '''
        If a restaurant is open and has space we should be able to book 
        tables.
        '''

        reference='Successful'
        covers=1
        start=datetime(2016, 5, 2, 13, 0)  # Monday 13.00
        finish=datetime(2016, 5, 2, 15, 0) # Monday 15.00

        restaurant_id = controller.restaurant_create(
            name='Safe',
            description='Example',
            opening_times=[
                ('Tuesday 12.00', 'Tuesday 16.00'),
            ],
            tables=[1]
        )

        booking_id = controller.booking_create(
            restaurant_id=restaurant_id,
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        self.assertIsNone(
            booking_id,
            'Making a booking should fail if the restaurant is closed.'
        )

##############################

    def test_booking_fails_when_restaurant_is_full(self):
        '''
        Bookings should fail if the restaurant has no space,
        even if the restaurant is open.
        '''

        reference='Successful'
        covers=1
        start=datetime(2016, 5, 2, 13, 0)  # Monday 13.00
        finish=datetime(2016, 5, 2, 15, 0) # Monday 15.00

        restaurant_id = controller.restaurant_create(
            name='Safe',
            description='Example',
            opening_times=[
                ('Monday 12.00', 'Monday 16.00'),
            ],
            tables=[1]
        )

        booking_id = controller.booking_create(
            restaurant_id=restaurant_id,
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        self.assertIsNotNone(
            booking_id,
            'We should be able to create a booking if the restaurant is open.'
        )

        booking_id = controller.booking_create(
            restaurant_id=restaurant_id,
            reference=reference,
            covers=covers,
            start=start,
            finish=finish
        )

        self.assertIsNone(
            booking_id,
            'Making a booking should fail if the restaurant is full.'
        )

###############################################################################

class ReportFunctionalTest(TestCase):
    '''
    We should be able to create a report showing the expected number of
    diners for a particular day.
    '''

    @given(
        name=text(),
        description=text(),
        opening_times=strategies.opening_times,
        tables=lists(integers(min_value=1, max_value=12)),
        date=datetimes()
    )
    def test_restaurant_in_report(
        self,
        name,
        description,
        opening_times,
        tables,
        date
    ):
        '''
        The restaurant should appear in the generated report.
        '''

        restaurant_id= controller.restaurant_create(
            name=name,
            description=description,
            opening_times=opening_times,
            tables=tables
        )

        restaurant = controller.restaurant_from_id(restaurant_id)

        report = controller.generate_report(restaurant_id, date)

        self.assertTrue(
            str(restaurant) in report,
            'A representation of the restaurant should appear in the report.'
        )
