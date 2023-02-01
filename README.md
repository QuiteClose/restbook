
Running the tests:

```bash
python3.5 setup.py test
```

Running the example:

```bash
python3.5 example.py
```

The example declares some tables and makes a few bookings. A report is printed
that will be similar to the following:

```
$ python3 example.py
Restaurant: Example Restaurant
Opening Period: Wednesday 17.00-Wednesday 23.00
Tables:
        None: []
        0: ['Lucas x1 @ 18.00']
        1: ['Sarah x2 @ 17.30']
        2: ['Angela x3 @ 17.30', 'Matthew x4 @ 20.15']
        3: ['Boris x5 @ 19.00']
```

