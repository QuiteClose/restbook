
import datetime
from unittest import TestCase

from hypothesis import assume, given
from hypothesis.strategies import integers, lists
from hypothesis.extra.datetime import datetimes

from restbook import entities, usecases
from restbook.time import MinuteOffset, get_dateinfo

###############################################################################

class RelevantBookingsTest(TestCase):

    @given(
        context=datetimes()
    )
    def test_bookings_discarded_if_out_of_bounds(self, context):
        '''
        Bookings that are out of bounds should not be in the returned list.
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

        kept = usecases.relevant_bookings(
            bookings=bookings,
            datetime_context=context,
            start_offset=start,
            end_offset=end,
        )

        self.assertListEqual(
            [x for x in bookings if x.reference == 'kept'],
            kept,
            'Bookings should be returned only if they are within the time window.'
        )

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
        tables=lists(integers(min_value=1, max_value=12))
    )
    def test_each_table_represented_in_plan(self, tables):
        '''
        The seating plan should have a key for each table given,
        this should be an empty list by default.
        '''

        plan = usecases.seating_plan(
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
        covers=integers(min_value=1, max_value=15),
        tables=lists(integers(min_value=1, max_value=12), min_size=5)
    )
    def test_single_booking_assigned_to_smallest_table(self, covers, tables):
        '''
        A single booking should be assigned to the smallest
        available table or None if no table is available.
        '''

        booking = entities.Booking(
            reference='kept',
            covers=covers,
            start=datetime.datetime.now(),
            finish=datetime.datetime.now(),
        )

        table_match = next((x for x in sorted(tables) if covers <= x), None)

        if table_match is not None:
            expected_table = tables.index(table_match)
        else:
            expected_table = None

        plan = usecases.seating_plan(
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


##############################

    @given(
        context=datetimes(),
        covers=integers(min_value=1, max_value=15),
    )
    def test_two_clashing_bookings_with_one_table(self, context, covers):
        '''
        If two bookings clash, the earlier booking should be assigned
        to a table and the later booking assinged to None.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        bookings = [
            entities.Booking(
                reference='earlier',
                covers=covers,
                start=datetime.datetime(year, month, day, 12, 0),
                finish=datetime.datetime(year, month, day, 13, 30),
            ),
            entities.Booking(
                reference='later',
                covers=covers,
                start=datetime.datetime(year, month, day, 12, 30),
                finish=datetime.datetime(year, month, day, 14, 0),
            )
        ]

        plan = usecases.seating_plan(
            tables=[covers],
            bookings=bookings
        )

        self.assertListEqual(
            plan[None],
            [x for x in bookings if x.reference == 'later'],
            'The later booking should be assigned to None if bookings clash.'
        )

        self.assertListEqual(
            plan[0],
            [x for x in bookings if x.reference == 'earlier'],
            'The earlier booking should get the table if bookings clash.'
        )

##############################

    @given(
        context=datetimes(),
        covers=integers(min_value=1, max_value=15),
    )
    def test_two_compatible_bookings_with_one_table(self, context, covers):
        '''
        Two bookings that do not clash should both be able to book a
        single table.
        '''

        year, month, day = context.year, context.month, context.day

        weekday = get_dateinfo(context).weekday

        start = entities.MinuteOffset.from_integers(weekday, 12, 0)
        end = entities.MinuteOffset.from_integers(weekday, 14, 0)

        bookings = [
            entities.Booking(
                reference='earlier',
                covers=covers,
                start=datetime.datetime(year, month, day, 12, 0),
                finish=datetime.datetime(year, month, day, 13, 0),
            ),
            entities.Booking(
                reference='later',
                covers=covers,
                start=datetime.datetime(year, month, day, 13, 0),
                finish=datetime.datetime(year, month, day, 14, 0),
            )
        ]

        plan = usecases.seating_plan(
            tables=[covers],
            bookings=bookings
        )

        self.assertListEqual(
            plan[None],
            [],
            'Bookings should not be assigned to None if they do not clash.'
        )

        self.assertListEqual(
            plan[0],
            bookings,
            'Bookings should be assigned to a table if they do not clash.'
        )

###############################################################################

class SpaceAvailableTest(TestCase):

    @given(
        tables=lists(integers(min_value=1, max_value=15))
    )
    def test_only_true_if_space_is_available(self, tables):
        '''
        space_available should only return True if there are enough tables.
        '''

        single_cover = entities.Booking(
            reference='Smallest possible',
            covers=1,
            start=datetime.datetime.now(),
            finish=datetime.datetime.now()
        )

        bookings = [
            entities.Booking(
                reference='Safe example',
                covers=covers,
                start=datetime.datetime.now(),
                finish=datetime.datetime.now()
            )
            for covers in tables
        ]

        self.assertTrue(
            usecases.space_available(
                requested_booking=single_cover,
                tables=tables,
                existing_bookings=bookings[1:]
            ),
            'space_available should return True if there are enough tables.'
        )

        self.assertFalse(
            usecases.space_available(
                requested_booking=single_cover,
                tables=tables,
                existing_bookings=bookings
            ),
            'space_available should return False if there are enough tables.'
        )

###############################################################################

class WithinTimesTest(TestCase):

    @given(
        context=datetimes(),
        start=datetimes(),
        finish=datetimes(),
    )
    def test_restaurant_open_true_only_if_restaurant_is_open(
        self,
        context,
        start,
        finish
    ):
        '''
        restaurant_open should return True if the restaurant is open.
        '''

        year, month, day = context.year, context.month, context.day

        start = start.replace(year=year, month=month, day=day)
        finish = finish.replace(year=year, month=month, day=day)

        assume(start < finish)

        start_info = get_dateinfo(start)
        finish_info = get_dateinfo(finish)

        open_for_given_times=entities.OpeningTimes(
            [(start_info.offset-1, finish_info.offset+1)]
        )

        closed_for_start=entities.OpeningTimes(
            [(start_info.offset+1, finish_info.offset+1)]
        )

        closed_for_finish=entities.OpeningTimes(
            [(start_info.offset-1, finish_info.offset-1)]
        )

        closed_for_both=entities.OpeningTimes(
            [(start_info.offset+1, finish_info.offset-1)]
        )

        self.assertTrue(
            usecases.within_times(open_for_given_times, start, finish),
            'within_times should return True if times are suitable.'
        )
        self.assertFalse(
            usecases.within_times(closed_for_start, start, finish),
            'within_times should return False if start time is unsuitable.'
        )

        self.assertFalse(
            usecases.within_times(closed_for_finish, start, finish),
            'within_times should return False if finish time is unsuitable.'
        )

        self.assertFalse(
            usecases.within_times(closed_for_both, start, finish),
            'within_times should return False if times are unsuitable.'
        )
