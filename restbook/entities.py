
'''Core types used by the application.'''

###############################################################################

from collections import UserList

###############################################################################

class Restaurant:
    '''
    A restaurant has a name and a description. It may also have
    opening times and a series of tables of different sizes.
    '''

    @classmethod
    def validate(cls, restaurant):
        '''
        Raises a ValueError if the given Restaurant does not pass tests
        for validation. Otherwise returns None.
        '''

        if not restaurant.name or str(restaurant.name) == '':
            raise ValueError

    def __init__(self, name, description='', opening_times=None, tables=None):
        self.name = name
        self.description = description
        self.opening_times = OpeningTimes(opening_times)
        self.tables = tables

    def is_valid(self):
        '''
        Calls Restaurant.validate on self. Catches any ValueErrors
        and returns True or False depending upon the result.
        '''
        try:
            self.validate(self)
        except ValueError:
            return False
        else:
            return True

###############################################################################

class OpeningTimes(UserList):
    '''
    OpeningTimes are represented as a list of tuples. Each tuple 
    represents an opening period as a pair of integers. Each integer
    is an offset in minutes since 0000 on Monday.
    '''

    @classmethod
    def validate(cls, opening_times):
        '''
        Raises a ValueError if the given OpeningTimes does not pass tests
        for validation. Otherwise returns None.
        '''

        pass

