
'''Basic time utilities used by the entities.'''

from collections import namedtuple
import datetime
import re

###############################################################################

DateInfo = namedtuple('DateInfo', ['datetime', 'year', 'week', 'weekday'])

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

