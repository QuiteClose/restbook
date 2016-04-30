
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
