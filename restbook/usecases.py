
'''Implements core functionality of the application.'''

from collections import OrderedDict, namedtuple

from restbook.entities import OpeningTimes
from restbook.time import get_dateinfo

###############################################################################

def relevant_bookings(bookings, datetime_context, start_offset, end_offset):
    '''
    Takes a list of bookings and returns a list of bookings that fall
    within a time window.

    The given datetime_context should be a datetime instance. This will
    be used to determine the year and week number that 0000 on Monday
    should be taken from. The given start_time and end_time should be
    of type MinuteOffset delimiting the window after 0000 on Monday
    that the time window represents.
    '''

    return [
        b for b in bookings
        if b.within(datetime_context, start_offset, end_offset)
    ]

###############################################################################

def seating_plan(tables, bookings):
    '''
    Generates a seating plan as a dictionary where the keys are table
    numbers and the values a list of bookings assigned to that table.

    The given tables should be a list of positive integers denoting a
    tables size. The table's number is taken from its index in the
    given list.

    Bookings which do not fit into the seating plan are assigned to a
    table with the key None and returned normally as part of the
    dictionary.
    '''

    IndexedTable = namedtuple('IndexedTable', ['index', 'covers'])

    plan = OrderedDict([(None, [])] + [(n, []) for n in range(len(tables))])

    indexed_tables = sorted(
        [
            IndexedTable(index=n, covers=tables[n])
            for n in range(len(tables))
        ],
        key=lambda x: x.covers
    )

    for booking in sorted(bookings, key=lambda x: x.covers):
        suitable_tables = (
            x for x in indexed_tables if booking.covers <= x.covers
        )

        for table in suitable_tables:
            if [x for x in plan[table.index] if booking.overlaps(x)]:
                continue
            else:
                plan[table.index].append(booking)
                break
        else:
            plan[None].append(booking)

    return plan

###############################################################################

def space_available(requested_booking, tables, existing_bookings):
    '''
    Takes a requested booking, a list of table sizes, and a list of
    already accepted bookings, and returns True or False depending upon
    whether a seating plan can be generated without displacing any
    existing bookings.
    '''

    if not tables:
        return False

    previous_overflow = seating_plan(tables, existing_bookings)[None]

    supposed_bookings = existing_bookings + [requested_booking]

    subsequent_overflow = seating_plan(tables, supposed_bookings)[None]

    return previous_overflow == subsequent_overflow

###############################################################################

def fulfills_times(opening_times, start, finish):
    '''
    Returns an OpeningTimes list from the given opening_times that
    fulfills the given start and finish datetimes. If the time window
    is not entirely covered by the given opening_times then an empty
    list is returned.
    '''
    start_offset = get_dateinfo(start).offset
    finish_offset = get_dateinfo(finish).offset

    fulfilled = [
        (time_opens, time_closes) for time_opens, time_closes in opening_times
        if start_offset >= time_opens and finish_offset <= time_closes
    ]

    '''
    Simple case: a single opening time fulfills the start and finish.
    '''

    if fulfilled:
        return OpeningTimes(fulfilled)

    '''
    Otherwise we need to check for a possible chain of adjacent opening times.
    '''

    adjacent_groups = []
    current_group = list()

    for n in range(len(opening_times)):
        time_opens, time_closes = opening_times[n]

        if not current_group:
            print('Appending to new list.')
            current_group.append(opening_times[n])
        elif current_group[-1][1] == time_opens-1:
            print('Appending to EXISTING list.')
            current_group.append(opening_times[n])
        else:
            print('Finished current_group.')
            adjacent_groups.append(current_group)
            current_group = list().append(opening_times[n])

    if current_group:
        adjacent_groups.append(current_group)

    for group in adjacent_groups:
        time_opens = group[0][0]
        time_closes = group[-1][1]

        if start_offset >= time_opens and finish_offset <= time_closes:
            return OpeningTimes(group)

    return OpeningTimes()

###############################################################################

def opens_within_times(opening_times, start, finish):
    '''
    Filters the given OpeningTimes object to only include opening times
    that start with the given start and finish datetimes.
    '''

    start_offset = get_dateinfo(start).offset
    finish_offset = get_dateinfo(finish).offset
    
    return OpeningTimes(
        [
            (time_opens, time_closes) for time_opens, time_closes in opening_times
            if start_offset <= time_opens and time_opens <= finish_offset
        ]
    )
