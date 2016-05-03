
'''Implements core functionality of the application.'''

from collections import OrderedDict, namedtuple

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

def within_times(opening_times, start, finish):
    '''
    Returns True if the given start and finish datetime types describe
    a time window within the given opening times.

    This function currently doesn't check for adjacent opening times so
    it may return False for 7 consecutive 24 hour opening times if the
    start and finish times cross midnight.
    '''

    start_info = get_dateinfo(start)
    finish_info = get_dateinfo(finish)

    for a, b in opening_times:
        if start_info.offset >= a and finish_info.offset <= b:
            return (a, b)

    return (None, None)
