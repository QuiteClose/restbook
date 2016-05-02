
from unittest import TestCase

from restbook import time 

###############################################################################

class MinuteOffsetUnitTest(TestCase):

    def test_minutes_in_week(self):
        '''
        Minutes in week must be accurate.
        '''

        self.assertEqual(
            time.MinuteOffset.MINUTES_IN_WEEK,
            60 * 24 * 7,
            'Minutes in week must equal 60 * 24 * 7.'
        )

##############################

    def test_conversion_from_strings(self):
        '''
        Should convert from 'Monday 00.00' to 0 or 'Monday 20.00' to 1200.
        '''

        sample = (
            (0, 'Monday 00.00'),
            (61, 'Monday 01.01'),
            (1200, 'Monday 20.00'),
            (3480, 'Wednesday 10.00'),
            (5250, 'Thursday 15.30'),
            (7020, 'Friday 21.00'),
            (10079, 'Sunday 23.59'),
            (10139, 'Sunday 24.59'), # hours should be able to wrap to next day
        )

        for example in sample:
            expected_result = example[0]
            given_string = example[1]

            self.assertEqual(
                expected_result,
                time.MinuteOffset.from_string(given_string),
                'MinuteOffset.from_string should convert '
                '"{string}" to {offset}.'.format(string=given_string,
                                                 offset=expected_result)
            )

##############################

    def test_failure_when_converting_invalid_strings(self):
        '''
        MinuteOffset.from_string should fail when given invalid day
        names or minutes that exceed 59.
        '''

        sample = (
            'Someday 00.00',
            'Monday 00.60',
        )

        for bad_example in sample:

            try:
                time.MinuteOffset.from_string(bad_example)
            except ValueError:
                pass
            else:
                self.fail(
                    'MinuteOffset.from_string should fail when '
                    'given "{invalid}".'.format(invalid=bad_example)
                )

