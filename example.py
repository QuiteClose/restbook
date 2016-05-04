from datetime import datetime

from restbook import controller

date = datetime.now()

restaurant_id = controller.restaurant_create(
    name='Example Restaurant',
    description='A restaurant used to demonstrate the restbook package.',
    opening_times=[
        ('Monday 17.00', 'Monday 23.00'),
        ('Tuesday 17.00', 'Tuesday 23.00'),
        ('Wednesday 17.00', 'Wednesday 23.00'),
        ('Thursday 17.00', 'Thursday 23.00'),
        ('Friday 17.00', 'Friday 23.00'),
        ('Saturday 17.00', 'Saturday 23.00'),
        ('Sunday 17.00', 'Sunday 23.00'),
    ],
    tables=[
        2, 2, 4, 6
    ]
)

controller.booking_create(
    restaurant_id=restaurant_id,
    reference='Angela',
    covers=3,
    start=date.replace(hour=17, minute=30),
    finish=date.replace(hour=20, minute=0),
)

controller.booking_create(
    restaurant_id=restaurant_id,
    reference='Lucas',
    covers=1,
    start=date.replace(hour=18, minute=0),
    finish=date.replace(hour=19, minute=30),
)

controller.booking_create(
    restaurant_id=restaurant_id,
    reference='Matthew',
    covers=4,
    start=date.replace(hour=20, minute=15),
    finish=date.replace(hour=22, minute=30),
)

controller.booking_create(
    restaurant_id=restaurant_id,
    reference='Sarah',
    covers=2,
    start=date.replace(hour=17, minute=30),
    finish=date.replace(hour=20, minute=30),
)

controller.booking_create(
    restaurant_id=restaurant_id,
    reference='Boris',
    covers=5,
    start=date.replace(hour=19, minute=0),
    finish=date.replace(hour=22, minute=30),
)

print(controller.generate_report(restaurant_id, date))
