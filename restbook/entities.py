
'''Core types used by the application.'''

###############################################################################

from collections import UserList
import re

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
        for validation. Otherwise returns True.
        '''

        if not restaurant.name or str(restaurant.name) == '':
            raise ValueError
        elif not restaurant.opening_times.is_valid():
            raise ValueError

        for table_size in restaurant.tables:
            if not isinstance(table_size, int) or table_size < 1:
                raise ValueError

        return True

##################################################

    def __init__(self, name, description='', opening_times=None, tables=None):
        self.name = name
        self.description = description
        if opening_times:
            self.opening_times = OpeningTimes(opening_times)
        else:
            self.opening_times = OpeningTimes()

        if tables:
            self.tables = list(tables)
        else:
            self.tables = list()

##############################

    def is_valid(self):
        '''
        Calls self.validate on self. Catches any ValueErrors
        and returns True or False depending upon the result.
        '''
        try:
            self.validate(self)
        except ValueError:
            return False
        else:
            return True

###############################################################################

class MinuteOffset(int):
    '''
    Times are given as an integer representing an offset in minutes
    since 0000 on Monday.
    '''

    MINUTES_IN_HOUR = 60
    MINUTES_IN_DAY = MINUTES_IN_HOUR * 24
    MINUTES_IN_WEEK = MINUTES_IN_DAY * 7

    DAY_NAMES = (
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    )

    '''
    Minute offsets can be converted from strings with the format
    'DAY HH.MM' where day is the long name of a day.
    '''
    STRING_PATTERN = r'^(?P<day>\w+) (?P<hour>\d\d)\.(?P<minute>\d\d)$'

    @classmethod
    def from_string(cls, string):
        '''
        Returns a MinuteOffset from the given string. Expects the given
        string to conform to the pattern 'DAY HH.MM' where day should be
        the long-name of the day. i.e. Monday or Wednesday.
        '''

        match = re.match(cls.STRING_PATTERN, string)

        if not match:
            raise ValueError

        day = match.group('day').capitalize()
        hour = int(match.group('hour'))
        minute = int(match.group('minute'))

        if day not in cls.DAY_NAMES:
            raise ValueError
        elif minute > 59:
            raise ValueError

        day_offset = cls.DAY_NAMES.index(day) * cls.MINUTES_IN_DAY
        hour_offset = hour * cls.MINUTES_IN_HOUR

        return cls(day_offset+hour_offset+minute)

###############################################################################

class OpeningTimes(UserList):
    '''
    OpeningTimes are represented as a list of tuples. Each tuple 
    represents an opening period as a pair of MinuteOffsets
    '''

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
        4. No start-time should be after it's end-time.
        '''

        if not len(opening_times):
            return True
        elif opening_times[0][0] < 0:
            raise ValueError
        elif opening_times[0][0] < (opening_times[-1][1]-MinuteOffset.MINUTES_IN_WEEK):
            raise ValueError

        previous_end_time = 0

        for period in opening_times:
            if period[0] < previous_end_time or period[0] > MinuteOffset.MINUTES_IN_WEEK:
                raise ValueError
            elif period[0] > period[1]:
                raise ValueError

            previous_end_time = period[1]

        return True

    def is_valid(self):
        '''
        Calls self.validate on self. Catches any ValueErrors
        and returns True or False depending upon the result.
        '''
        try:
            self.validate(self)
        except ValueError:
            return False
        else:
            return True
        pass

