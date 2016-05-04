from setuptools import setup

setup(
    name='restbook',
    author='dsclose',
    version='0.1',
    description='Manages restaurant bookings and seating plans.',
    packages=['restbook'],
    test_suite='nose.collector',
    install_requires=[],
    tests_require=[
        'hypothesis',
        'nose',
        'pytz',
        'tox',
    ],
)
