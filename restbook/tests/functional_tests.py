
from datetime import datetime
from unittest import TestCase
import uuid

from hypothesis import assume, given
from hypothesis.extra.datetime import datetimes
from hypothesis.strategies import integers, lists, text

from restbook import controller, entities, usecases
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
    def test_restaurant_name_in_report(
        self,
        name,
        description,
        opening_times,
        tables,
        date
    ):
        '''
        The restaurant name should appear in the generated report.
        '''

        assume(name != '')

        restaurant_id= controller.restaurant_create(
            name=name,
            description=description,
            opening_times=opening_times,
            tables=tables
        )

        report = controller.generate_report(restaurant_id, date)

        self.assertTrue(
             name in report,
            'The restaurant name should appear in the report.'
        )

##############################

    @given(
        date=datetimes(),
        opening_times=strategies.opening_times_strings
    )
    def test_opening_times_in_report(
        self,
        date,
        opening_times
    ):
        '''
        The opening times for a given day should appear in the report.
        '''

        start_of_day = date.replace(hour=0, minute=0)
        end_of_day = date.replace(hour=23, minute=59)

        restaurant_id= controller.restaurant_create(
            name='Safe',
            description='Example',
            opening_times=opening_times,
            tables=[]
        )

        report = controller.generate_report(restaurant_id, date)

        matching_times = usecases.opens_within_times(opening_times, start_of_day, end_of_day)

        for opening_time, closing_time in matching_times:
            assert('{}-{}'.format(opening_time, closing_time) in report)

##############################

    @given(
        date=datetimes(),
        tables=lists(integers(min_value=1, max_value=15), min_size=1)
    )
    def test_bookings_appear_in_report(
        self,
        date,
        tables
    ):
        '''
        The bookings for a given day should appear in the report.
        '''

        start_of_day = date.replace(hour=0, minute=0)
        end_of_day = date.replace(hour=23, minute=59)

        restaurant_id= controller.restaurant_create(
            name='Safe',
            description='Example',
            opening_times=entities.OpeningTimes(
                [
                    ('Monday 00.00', 'Monday 23.59'),
                    ('Tuesday 00.00', 'Tuesday 23.59'),
                    ('Wednesday 00.00', 'Wednesday 23.59'),
                    ('Thursday 00.00', 'Thursday 23.59'),
                    ('Friday 00.00', 'Friday 23.59'),
                    ('Saturday 00.00', 'Saturday 23.59'),
                    ('Sunday 00.00', 'Sunday 23.59'),
                ]
            ),
            tables=tables
        )

        bookings = [
            entities.Booking(
                reference=str(uuid.uuid1()),
                covers=covers,
                start=date,
                finish=date
            )
            for covers in tables
        ]

        for booking in bookings:
            controller.booking_create(
                restaurant_id=restaurant_id,
                reference=booking.reference,
                covers=booking.covers,
                start=booking.start,
                finish=booking.finish
            )

        report = controller.generate_report(restaurant_id, date)

        for booking in bookings:
            assert('{} x{}'.format(booking.reference, booking.covers) in report)

