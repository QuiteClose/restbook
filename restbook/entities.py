
'''Core types used by the application.'''

###############################################################################

from collections import UserList

from restbook.time import MinuteOffset, get_dateinfo

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
            raise ValueError('Restaurants must have a name.')
        elif not restaurant.opening_times.is_valid():
            raise ValueError('Opening times must be valid.')

        for table_size in restaurant.tables:
            if not isinstance(table_size, int) or table_size < 1:
                raise ValueError('Table sizes must be positive integers.')

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

    def __str__(self):
        output = []

        output.append('Restaurant: {}'.format(self.name))
        output.append('Description: {}'.format(self.description))

        if self.tables:
            output.append('Tables:')
            for n in range(len(self.tables)):
                output.append(
                    '\t{table_number}: {covers}'.format(
                        table_number=n,
                        covers=self.tables[n]
                    )
                )
        else:
            output.append('Tables: None')

        output.append('Opening-Times: ' + str(self.opening_times))

        return '\n'.join(output)

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
            raise ValueError('First opening time cannot start in previous week.')
        elif opening_times[0][0] < (opening_times[-1][1]-MinuteOffset.MINUTES_IN_WEEK):
            raise ValueError('First opening time cannot start in following week.')

        previous_end_time = 0

        for period in opening_times:
            if period[0] < previous_end_time:
                raise ValueError('Opening times must be sequential.')
            if period[0] > MinuteOffset.MINUTES_IN_WEEK:
                raise ValueError('Opening times must not start in following week.')
            elif period[0] > period[1]:
                raise ValueError('Opening times must start before they finish.')

            previous_end_time = period[1]

        return True

    def __init__(self, given=None):
        '''
        Takes a list of tuples, each representing a pair of
        MinuteOffsets. A single integer is enough to represent an
        offset. If a string is provided a conversion will be attempted
        which may raise a ValueError. If an iterable is provided then
        a conversion from integers will be attempted which may also
        raise a ValueError.
        '''

        def convert(n):
            if isinstance(n, str):
                return MinuteOffset.from_string(n)
            try:
                iter(n)
            except TypeError:
                return MinuteOffset(n)
            else:
                return MinuteOffset.from_integers(*n)

        if given is None:
            given = []

        super().__init__((convert(a), convert(b)) for a, b in given)

##############################

    def __str__(self):
        return ' '.join(
            '{start}-{end}'.format(start=str(start), end=str(end))
            for start, end in self
        )

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

class Booking:
    '''
    A booking has a reference that may or may not be unique. It also
    has a number of covers (guests) and a start and finish-time
    represented using datetime objects.
    '''

    @classmethod
    def validate(cls, booking):

        if booking.start > booking.finish:
            raise ValueError('Booking must start before it finishes.')

    def __init__(self, reference, covers, start, finish):
        self.reference = reference
        self.covers = covers
        self.start = start
        self.finish = finish

    def __str__(self):
        return '{reference} x{covers} @ {hour:02d}.{minute:02d}'.format(
            reference=self.reference,
            covers=self.covers,
            hour=self.start.hour,
            minute=self.start.minute
        )

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

##############################

    def within(self, datetime_context, start_time, end_time):
        '''
        Returns True or False depending upon whether the booking
        falls within the given start_time and end_time.

        The given start_time and end_time should be the MinuteOffset
        since 0000 on Monday. The given datetime_context determines
        which week the start_time and end_time refer to.
        '''

        context = get_dateinfo(datetime_context)
        start_context = get_dateinfo(self.start)
        finish_context = get_dateinfo(self.finish)

        if context.week != start_context.week:
            return False

        if start_context.offset >= start_time and \
            finish_context.offset <= end_time:
            return True
        else:
            return False

##############################

    def overlaps(self, booking):
        '''
        Returns True or False depending upon whether the given booking
        overlaps self.
        '''

        return self.start < booking.finish and self.finish > booking.start
