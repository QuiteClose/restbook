
'''Core types used by the application.'''

###############################################################################


class Restaurant:
    '''
    A restaurant has a name and a description. It may also have
    opening times and a series of tables of different sizes.
    '''

    @classmethod
    def validate(cls, restaurant):
        pass

    def __init__(self, name, description='', opening_times=None, tables=None):
        self.name = name
        self.description = description
        self.opening_times = opening_times
        self.tables = tables

    def is_valid(self):
        '''
        Calls Restaurant.validate on self. Catches any ValueErrors
        and returns True or False depending upon the result.
        '''
        try:
            self.validate(self)
        except ValueError:
            return False
        else:
            return True
