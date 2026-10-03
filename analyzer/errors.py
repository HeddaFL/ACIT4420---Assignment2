'''
Purpose: give my program a way to raise errors when the data is bad/rejected.
This module contains exceptions or errors for option a: the fitness analyzer.
'''

# For bad ID formats.
class InvalidIdentifierError(ValueError):

    def __init__(self, field, value):
        self.field = field # remember which field (column) that failed
        self.value = value # remember the bad value 
        super().__init__(f'Invalid Identifier: ({field}:{value!r})') # the '!r' ensures that the data is shown exactly as it is. 

# For any other unacceptable rows in the data.
class InvalidRecordError(ValueError):

    def __init__(self, field, reason):
        self.field = field # remember which field (column) that failed
        self.reason = reason # remember why it failed
        super().__init__(f'Invalid Record: ({field}:{reason})') 

# For any errors with the files. 
class DataFileError(Exception):
    pass
