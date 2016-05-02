
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

    MINUTES_IN_WEEK = 60 * 24 * 7

    @classmethod
    def validate(cls, opening_times):
        '''
        Raises a ValueError if the given OpeningTimes does not pass
        tests for validation. Otherwise returns True.

        Zero-length opening times are valid. Otherwise OpeningTimes
        must conform to the following rules:

        1. The first start-time must be >= 0
        2. No start-time should be < the previous end-time
        3. No start-time should be after the end of the week.
        '''

        if not len(opening_times):
            return True
        elif opening_times[0][0] < 0:
            raise ValueError
        elif opening_times[0][0] < (opening_times[-1][1]-cls.MINUTES_IN_WEEK):
            raise ValueError

        previous_end_time = 0

        for period in opening_times:
            if period[0] < previous_end_time or period[0] > cls.MINUTES_IN_WEEK:
                raise ValueError

            previous_end_time = period[1]

        return True

