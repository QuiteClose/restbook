
import datetime
from unittest import TestCase

from restbook import entities, usecases

###############################################################################

class SeatingPlanUnitTest(TestCase):

    def test_bookings_assigned_to_None_if_no_tables(self):
        '''
        When a restaurant has no tables all bookings should be assigned
        to the key None.
        '''

        # Monday 2nd May 2016
        year = 2016
        month = 5
        day = 2

        start_time = entities.MinuteOffset.from_string('Monday 00.00')
        end_time = entities.MinuteOffset.from_string('Sunday 23.59')

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
            year=year,
            month=month,
            day=day,
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


