from setuptools import setup

setup(
    name='restbook',
    version='0.1',
    description='Manages restaurant bookings and seating plans.',
    packages=['restbook'],
    install_requires=[],
    tests_require=[
        'hypothesis',
    ],
    test_suite='restbook.tests'
)
