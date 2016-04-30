
'''Core types used by the application.'''

###############################################################################


class Restaurant:
    '''
    A restaurant has a name and a description. It may also have
    opening times and a series of tables of different sizes.
    '''

    def __init__(self, name, description, opening_times=None, tables=None):
        self.name = name
        self.description = description
        self.opening_times = opening_times
        self.tables = tables

    def is_valid(self):
        return True
