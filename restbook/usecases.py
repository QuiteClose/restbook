
'''Implements core functionality of the application.'''

from collections import OrderedDict, namedtuple

###############################################################################

def seating_plan(datetime_context, start_time, end_time, tables, bookings):
    '''
    Generates a seating plan as a dictionary where the keys are table
    numbers and the values a list of bookings assigned to that table.

    The given tables should be a list of positive integers denoting a
    tables size. The table's number is taken from its index in the
    given list.

    The given datetime_context should be a datetime instance. This will
    be used to determine the year and week number that 0000 on Monday
    should be taken from. The given start_time and end_time should be
    of type MinuteOffset delimiting the window after 0000 on Monday
    that the seating plan should represent. Any bookings which do not
    fall within the time window are discarded.

    Bookings which fall within the time window but cannot be assigned a
    table because of space will be assigned to the table None, and
    returned normally as part of the dictionary.
    '''

    IndexedTable = namedtuple('IndexedTable', ['index', 'covers'])

    plan = OrderedDict([(None, [])] + [(n, []) for n in range(len(tables))])

    indexed_tables = sorted(
        [
            IndexedTable(index=n, covers=tables[n])
            for n in range(len(tables))
        ],
        key=lambda x: x.covers,
    )

    relevant_bookings = sorted(
        [
            b for b in bookings
            if b.within(datetime_context, start_time, end_time)
        ],
        key=lambda x: x.covers,
        reverse=True
    )

    for booking in relevant_bookings:
        suitable_tables = (
            x for x in indexed_tables if booking.covers <= x.covers
        )

        for table in suitable_tables:
            if plan[table.index]:
                continue
            else:
                plan[table.index].append(booking)
                break
        else:
            plan[None].append(booking)

    return plan

