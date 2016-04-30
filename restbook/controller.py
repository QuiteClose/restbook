
from collections import namedtuple
from uuid import uuid1 as generate_id

###############################################################################

_restaurants = {}

###############################################################################

Restaurant = namedtuple(
    'Restaurant',
    ['id', 'name', 'description', 'opening_times', 'tables']
)

###############################################################################

def restaurant_create(name, description, opening_times=None, tables=None):
    id = generate_id()

    _restaurants[id] = Restaurant(id, name, description, opening_times, tables)

    return id

##############################

def restaurant_from_id(id):
    try:
        return _restaurants[id]
    except KeyError:
        return None
