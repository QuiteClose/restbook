
def seating_plan(year, month, day, start_time, end_time, tables, bookings):
    '''
    Generates a seating plan as a dictionary where the keys are table
    numbers and the values a list of bookings assigned to that table.

    The given tables should be a list of positive integers denoting a
    tables size. The table's number is taken from its index in the
    given list.

    The given year, month and day should be integers describing a date.
    The given start_time and end_time should be MinuteOffets describing
    the window on that date to generate a seating plan for. Any bookings
    which do not start and finish within that window are discarded.

    Bookings which fall within the time window but cannot be assigned a
    table because of space will be assigned to the table None, and
    returned normally as part of the dictionary.
    '''

    return {}
