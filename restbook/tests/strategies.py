
'''
Custom strategies for use with the Hypothesis test framework.
'''

from restbook.time import MinuteOffset

from hypothesis.strategies import integers, lists, tuples
from hypothesis.strategies import composite

MINUTES_IN_WEEK = 10080

'''
Opening times are a list of time periods, each of those being start and
end times defined in terms of minutes since 0000 hours on Monday. There
are 10080 minutes in a week, so the start-time of the first element
should not-exceed that number. Opening times should not overlap, so
the end-time of a period should not exceed the start-time of the
subsequent period. This extends to weekly overlaps, so the end-time
of the last element should not wrap around to exceed the start-time of
the first.

The hypothesis composite strategy provides a draw function to generate
examples from strategies. When generating test data for opening times,
we will need a way to generate time periods using this draw function.
'''

def _random_time(draw, min_value, max_value):
    '''
    Uses the given draw function to obtain an integer within the bounds
    of the given min_value and max_value.
    '''
    return draw(integers(min_value=min_value, max_value=max_value)).real


def _random_time_period(draw, min_value, max_value, overlap):
    '''
    Uses the given draw function to obtain a tuple of two integers. The
    first element will always be bounded by min_value and max_value. The
    second element will be bounded by the first element and the sum of
    max_value and overlap.
    '''

    start = _random_time(draw, min_value, _random_time(draw, min_value, max_value))
    end = _random_time(draw, start, max_value+overlap)

    return start, end


@composite
def opening_times_sample(
    draw,
    min_value=0,
    max_value=MINUTES_IN_WEEK,
    max_overlap=0
):
    '''
    Generates a list of an arbitrary length with each element being a
    tuple of two integers. The tuples represent time periods as a pair
    of integers. Each integer represents the number of minutes since
    0000 on Monday, with the first integer being the start-time and the
    second integer being the end-time. The returned list conforms to the
    following rules:

    1. The start-time of the first element will be greater-than-or-
       equal-to the given min_value and less-than-or-equal-to the given
       max_value.
    2. The end-time of last element will be less-than-or-equal-to the sum
       of the given max_value and max_overlap.
    3. The end-time of any element will be greater-than-or-equal-to the
       start-time of that element.
    4. 

    1. The end-time for any period will never be less than the start-time
       of that period.
    2. The start-time for any period will never be less than the end-time
       of the previous period.
    3. The end-time of the last period will always be less than 10080 +
       max_overlap. This allows periods to end after 23.59 on Sunday
    '''

    example = []

    previous_endtime = 0

    while previous_endtime < MINUTES_IN_WEEK:
        period = _random_time_period(
            draw=draw,
            min_value=previous_endtime,
            max_value=MINUTES_IN_WEEK,
            overlap=max_overlap
        )

        example.append(period)
        previous_endtime = period[1]

    return example


'''
The opening_times strategy we shall use will incorporate a small overlap
and will filter the results so that the end-time of the last element does
not overlap the start-time of the first element.
'''

opening_times = opening_times_sample(
    max_overlap = 440
).filter(lambda x: x[0][0] > (x[-1][1] - MINUTES_IN_WEEK))




opening_times_strings = opening_times.map(
    lambda x: [(str(MinuteOffset(n[0])), str(MinuteOffset(n[1]))) for n in x]
)

