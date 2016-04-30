
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from . import controller

###############################################################################

class _AbstractControllerTest:
    '''
    Abstract testcase for any controller based tests.
    '''

    def setUp(self):
        self.controller = controller


###############################################################################

class ControllerFunctionalTest(_AbstractControllerTest, TestCase):
    '''
    Functional tests for a controller module.
    '''

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


###############################################################################

class ControllerUnitTest(_AbstractControllerTest, TestCase):
    '''
    Unit tests for the controller module
    '''

    def test_has_expected_attributes(self):
        '''
        Each controller should provide a minimum set of attributes.
        '''

        feeback = 'Controller module "{module}" should have attribute "{attr}"'
        expected = (
            'restaurant_create',
            'restaurant_from_id',
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
