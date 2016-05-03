
from datetime import datetime
from unittest import TestCase

from hypothesis import assume, given
from hypothesis.strategies import text

from restbook import controller

###############################################################################

class ControllerUnitTest(TestCase):
    '''
    Unit tests for the controller module
    '''

    def setUp(self):
        self.controller = controller

    def test_has_expected_attributes(self):
        '''
        Each controller should provide a minimum set of attributes.
        '''

        feeback = 'Controller module "{module}" should have attribute "{attr}"'
        expected = (
            'restaurant_create',
            'restaurant_from_id',
            'booking_create',
            'booking_from_id',
        )

        for attribute in expected:
            self.assertTrue(
                hasattr(self.controller, attribute),
                feeback.format(module=self.controller.__name__, attr=attribute)
            )

##############################

    @given(name=text(), description=text())
    def test_can_create_restaurants(self, name, description):
        '''
        Using just a name and a description, we should be able to
        create restaurants.
        '''

        assume(name != '')

        unique_id = self.controller.restaurant_create(
            name=name,
            description=description
        )

        assert(unique_id is not None)

##############################

    @given(name=text(), description=text())
    def test_can_retreive_created_restaurants(self, name, description):
        '''
        After creating a restaurant we should be able to retreive it.
        '''

        assume(name != '')

        unique_id = self.controller.restaurant_create(
            name=name,
            description=description
        )

        if unique_id:
            restaurant = self.controller.restaurant_from_id(unique_id)
            assert(restaurant.name == name)
            assert(restaurant.description == description)

##############################

    def test_cannot_create_restaurants_without_a_name(self):
        unique_id = self.controller.restaurant_create(
            name='',
            description='Example Description'
        )

        self.assertIsNone(
            unique_id,
            'Restaurant creation should fail if no name is provided.'
        )

##############################

    def test_can_create_bookings(self):
        '''
        We should be able to create bookings if the restaurant has
        space.
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

##############################

    def test_can_retreive_created_bookings(self):
        '''
        After creating a booking we should be able to retreive it.
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

        if booking_id:
            booking = self.controller.booking_from_id(booking_id)
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

