
'''A controller that stores restaurants and bookings in memory.'''

###############################################################################

from uuid import uuid1 as generate_id

##############################

from . import entities

###############################################################################

''' Restaurants and bookings are stored in dictionaries with their
unique id acting as the key.
'''

_restaurants = {}
_bookings = {}

###############################################################################

def restaurant_create(name, description, opening_times=None, tables=None):
    '''
    Takes the properties of a restaurant, generates a UUID for it and,
    if that restaurant passes validation, stores it for later retreival.
    If a restaurant is successfully stored, its UUID is returned.
    Otherwise, the return value is None.
    '''

    id = generate_id()

    restaurant = entities.Restaurant(
        name=name,
        description=description,
        opening_times=opening_times,
        tables=tables
    )

    if restaurant.is_valid():
        _restaurants[id] = restaurant
        return id
    else:
        return None

##############################

def restaurant_from_id(id):
    '''
    Attempts to retreive a Restaurant according to the UUID returned by
    restaurant_create. Returns that Restaurant if found, otherwise
    returns None.
    '''

    try:
        return _restaurants[id]
    except KeyError:
        return None

###############################################################################

def booking_create(restaurant_id, reference, covers, start, finish):

    id = generate_id()

    booking = entities.Booking(
        reference=reference,
        covers=covers,
        start=start,
        finish=finish
    )

    _bookings[id] = booking

    return id

##############################

def booking_from_id(id):
    '''
    Attempts to retreive a Booking according to the UUID returned by
    booking_create. Returns that Booking if found, otherwise returns
    None.
    '''

    try:
        return _bookings[id]
    except KeyError:
        return None
