"""
Purpose: checks for valid ID (participant and session) format,
type of data and check the range. If they are not valid, raise exceptions/errors. 
"""

# imports
import math
import re
from .errors import InvalidIdentifierError, InvalidRecordError


# create attributes for regular expresion patterns
PARTICIPANT_REG_PATTERN = re.compile(r'^P\d{3}$') # the regular expression is defined in the assignment text.
SESSION_REG_PATTERN = re.compile(r'^FIT-\d{4}-\d{3}$') # the regular expression is defined in the assignment text.

# The participant ID needs to be a match on the format to the IDs. 
# Therefore, i need to use regular expression to ensure that the ID match the format of the regular expression.

def check_valid_participant_id(value):
    if not PARTICIPANT_REG_PATTERN.fullmatch(value):
        raise InvalidIdentifierError('participant_id', value)
    return value

def check_valid_session_id(value):
    if not SESSION_REG_PATTERN.fullmatch(value):
        raise InvalidIdentifierError('session_id', value)
    return value

# The file fitness_sessions_invalid.csv has examples of "fast" and "two" with text.
# The data needs to be numbers, so to ensure that only numbers are valid, we need a function that can 
# ensure that a InvalidRecordError is raised if the data do not have a number. The function to_int and to_float are made to ensure this. 

def to_int(field, raw):
    try:
        return int(raw)
    except ValueError:
        raise InvalidRecordError(field, f'Cannot convert {raw!r} into int value.') from None

def to_float(field, raw):
    try:
        number = float(raw)
    except ValueError:
        raise InvalidRecordError(field, f'Cannot convert {raw!r} into float value.') from None
    if not math.isfinite(number): # ensure that if 'inf' or 'nan' is a text in the csv data, it will be rejected.
        raise InvalidRecordError(field, f'{raw!r} is not a finite number.')
    return number

# To ensure impossible or invalid data does not become a part of the results. I need to exclude 
# some values through a range. This is what the function range_check do. 

# I will also make attributes with a fixed range.
# This is based on having the ranges wide enough to accept valid rows, but still reject impossible rows.  

HEART_RATE_RANGE = (35, 205) # BPM, rejects -15 and 999.
TEMPERATURE_RANGE = (25, 42) # Celsius, plausible skin temperature, will reject 55.0

ACTIVITY_LEVEL_RANGE = (0.0, 1.0) # DATA_DICTIONARY.txt defines this range as 0 to 1
SIGNAL_QUALITY_RANGE = (0.0, 1.0) # DATA_DICTIONARY.txt defines this range as 0 to 1

SKIN_RESPONSE_RANGE = (0.0, float('inf')) # DATA_DICTIONARY.txt defines this range as non-negative with no upper limit
TIMESTAMP_RANGE = (0, float('inf')) # DATA_DICTIONARY.txt defines this range as non-negative observed index

def range_check(field, value, low, high):
    if not (low <= value <= high):
        raise InvalidRecordError(field, f'{value} is outside of the range ({low} to {high})')
    return value
