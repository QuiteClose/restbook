
import datetime
from unittest import TestCase

from hypothesis import given
from hypothesis.extra.datetime import datetimes

from restbook import entities, usecases
from restbook.time import MinuteOffset, get_dateinfo

###############################################################################

class SeatingPlanUnitTest(TestCase):

    def test_bookings_assigned_to_None_if_no_tables(self):
        '''
        When a restaurant has no tables all bookings should be assigned
        to the key None.
        '''

        # Monday 2nd May 2016
        context = datetime.datetime(2016, 5, 2)
        year, month, day = context.year, context.month, context.day

        start_time = MinuteOffset.from_string('Monday 00.00')
        end_time = MinuteOffset.from_string('Sunday 23.59')

        bookings = [
            entities.Booking(
                reference='0',
                covers=1,
                start=datetime.datetime(year, month, day, 0, 0),
                finish=datetime.datetime(year, month, day, 1, 0),
            ),
            entities.Booking(
                reference='1',
                covers=1,
                start=datetime.datetime(year, month, day+1, 12, 0),
                finish=datetime.datetime(year, month, day+1, 20, 0),
            )
        ]

        plan = usecases.seating_plan(
            datetime_context=context,
            start_time=start_time,
            end_time=end_time,
            tables=[],
            bookings=bookings
        )

        self.assertDictEqual(
            {None: bookings},
            plan,
            'Valid bookings should be assigned to table None when no '
            'table is available.'
        )


    @given(
        context=datetimes()
    )
    def test_bookings_discarded_if_out_of_bounds(self, context):
        '''
        Bookings that are out of bounds should not be in the dictionary
        that is returned.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        bookings = [
            entities.Booking(
                reference='discarded_starts_too_soon',
                covers=1,
                start=datetime.datetime(year, month, day, 11, 0),
                finish=datetime.datetime(year, month, day, 13, 0),
            ),
            entities.Booking(
                reference='discarded_starts_too_late',
                covers=1,
                start=datetime.datetime(year, month, day, 14, 30),
                finish=datetime.datetime(year, month, day, 15, 0),
            ),
            entities.Booking(
                reference='discarded_finishes_too_late',
                covers=1,
                start=datetime.datetime(year, month, day, 13, 30),
                finish=datetime.datetime(year, month, day, 15, 0),
            ),
            entities.Booking(
                reference='kept',
                covers=1,
                start=datetime.datetime(year, month, day, 12, 0),
                finish=datetime.datetime(year, month, day, 14, 0),
            ),
            entities.Booking(
                reference='kept',
                covers=1,
                start=datetime.datetime(year, month, day, 12, 0),
                finish=datetime.datetime(year, month, day, 13, 0),
            ),
            entities.Booking(
                reference='kept',
                covers=1,
                start=datetime.datetime(year, month, day, 13, 0),
                finish=datetime.datetime(year, month, day, 14, 0),
            )
        ]

        plan = usecases.seating_plan(
            datetime_context=context,
            start_time=start,
            end_time=end,
            tables=[],
            bookings=bookings
        )

        self.assertDictEqual(
            {None: [x for x in bookings if x.reference == 'kept']},
            plan,
            'Bookings should be discarded if they are not within time.'
        )

