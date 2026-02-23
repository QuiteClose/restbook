# Restbook

An experiment after reading some Uncle Bob. This was a long time ago, and since then I've found that three layers of abstraction are usually sufficient:

1.  A base/utility layer to sit in-front of APIs, storage, etc.
2.  An adapter layer to present those utilities in a domain-specific way.
3.  General business logic written in terms of the adapters.

In such cases, the controller is just the entry-point and can be a thin layer on-top. This project tries to take Uncle Bob at his word and perhaps suffers for it. Maybe if I was using a purely functional language I'd feel differently?


## Structure

```
example.py
    └── controller.py      Orchestration and in-memory persistence
            ├── entities.py    Domain models: Restaurant, Booking, OpeningTimes
            ├── usecases.py    Pure business logic: seating plans, availability
            └── time.py        Week-offset time representation
```

The seating algorithm assigns each booking to the smallest available table with no time overlap.

## Usage

```bash
python3 example.py
```

```
Restaurant: Example Restaurant
Opening Period: Wednesday 17.00-Wednesday 23.00
Tables:
        None: []
        0: ['Lucas x1 @ 18.00']
        1: ['Sarah x2 @ 17.30']
        2: ['Angela x3 @ 17.30', 'Matthew x4 @ 20.15']
        3: ['Boris x5 @ 19.00']
```

## Tests

```bash
pip install -e ".[test]"
python -m pytest
```

Uses [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing.

## Tech

Python 3. No external runtime dependencies.
