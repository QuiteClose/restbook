
import datetime
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import integers, lists
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

##############################

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

##############################

    @given(
        tables=lists(integers(min_value=1, max_value=12))
    )
    def test_each_table_represented_in_plan(self, tables):
        '''
        The seating plan should have a key for each table given,
        this should be an empty list by default.
        '''

        plan = usecases.seating_plan(
            datetime_context=datetime.datetime.now(),
            start_time=0,
            end_time=0,
            tables=tables,
            bookings=[]
        )

        self.assertEqual(
            len([None] + tables),
            len(plan.keys()),
            'A seating plan should have a key for each table given.'
        )

        for key in plan:
            self.assertListEqual(
                plan[key],
                [],
                'A seating plan should yield an empty list for each table when '
                'no bookings are given.'
            )

##############################

    @given(
        context=datetimes(),
        covers=integers(min_value=1, max_value=15),
        tables=lists(integers(min_value=1, max_value=12))
    )
    def test_single_booking_assigned_to_smallest_table(
        self,
        context,
        covers,
        tables
    ):
        '''
        A single booking should be assigned to the smallest
        available table or None if no table is available.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        booking = entities.Booking(
            reference='kept',
            covers=covers,
            start=datetime.datetime(year, month, day, 12, 30),
            finish=datetime.datetime(year, month, day, 13, 30),
        )

        table_match = next((x for x in tables if x <= covers), None)

        if table_match is not None:
            expected_table = tables.index(table_match)
        else:
            expected_table = None

        plan = usecases.seating_plan(
            datetime_context=context,
            start_time=start,
            end_time=end,
            tables=tables,
            bookings=[booking]
        )

        assert(expected_table in plan)

        self.assertListEqual(
            plan[expected_table],
            [booking],
            'A single booking should be assigned to the first table that fits '
            'or None if no table is suitable.'
        )


