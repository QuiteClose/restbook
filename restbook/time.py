
'''Basic time utilities used by the entities.'''

from collections import namedtuple
import datetime
import re

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
    STRING_FORMAT = '{day} {hour:02d}.{minute:02d}'
    STRING_PATTERN = r'^(?P<day>\w+) (?P<hour>\d\d)\.(?P<minute>\d\d)$'

    @classmethod
    def from_integers(cls, day, hour, minute):
        '''
        Returns a MinuteOffset from the given day, hour and minute
        offsets.

        Raises a ValueError if any of the fields are less-than 0, if
        day is greather-than 6 or if minute is greater-than 59.
        '''

        if day > 6:
            raise ValueError('Given day must be in range 0..6')
        elif minute > 59:
            raise ValueError('Given minute must be in range 0..59')

        if day < 0 or hour < 0 or minute < 0:
            raise ValueError('Given values must be 0 or greater.')

        day_offset = day * cls.MINUTES_IN_DAY
        hour_offset = hour * cls.MINUTES_IN_HOUR

        return cls(day_offset+hour_offset+minute)

##############################

    @classmethod
    def from_string(cls, string):
        '''
        Returns a MinuteOffset from the given string. Expects the given
        string to conform to the pattern 'DAY HH.MM' where day should be
        the long-name of the day. i.e. Monday or Wednesday.
        '''

        match = re.match(cls.STRING_PATTERN, string)

        if not match:
            raise ValueError(
                'Given string must conform to pattern {}'.format(
                    cls.STRING_FORMAT
                )
            )

        day = match.group('day').capitalize()
        hour = int(match.group('hour'))
        minute = int(match.group('minute'))

        return cls.from_integers(cls.DAY_NAMES.index(day), hour, minute)

##############################

    def __str__(self):
        '''
        Converts an offset into a string in the form of DAY HH.MM. If
        the offset carries into the next week, then the day will appear
        as Sunday with the hours exceeding 24.
        '''

        day = self // self.MINUTES_IN_DAY

        if day > 6:
            day = 6

        day_offset = day * self.MINUTES_IN_DAY

        hour = (self-day_offset) // self.MINUTES_IN_HOUR
        hour_offset = hour * self.MINUTES_IN_HOUR

        minute = self - day_offset - hour_offset

        return self.STRING_FORMAT.format(
            day=self.DAY_NAMES[day],
            hour=hour,
            minute=minute
        )


###############################################################################

'''
The DateInfo tuple provides the year, week number and weekday number
described by a particular datetime. The MinuteOffset since the start of
that week is stored in the offset field. This tuple should be used where
weekday or week numbers are needed to ensure that data is calculated
uniformly for comparisons.
'''

DateInfo = namedtuple('DateInfo', 
                      ['datetime', 'year', 'week', 'weekday', 'offset'])

##############################

def get_dateinfo(datetime_context):
    '''
    Return a DateInfo tuple from the given datetime.
    '''

    year, week, iso_day = datetime_context.isocalendar()
    weekday = iso_day - 1

    offset = MinuteOffset.from_integers(
        weekday, 
        datetime_context.hour,
        datetime_context.minute
    )

    return DateInfo(
        datetime=datetime_context,
        year=year,
        week=week,
        weekday=weekday,
        offset=offset
    )

