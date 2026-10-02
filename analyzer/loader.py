"""
Purpose: turn the csv files into objects. 
"""

# imports
import csv
from pathlib import Path
from .errors import DataFileError, InvalidIdentifierError, InvalidRecordError
from .validators import check_valid_participant_id, check_valid_session_id
from .models import Participant, Observation, Session

'''
participants.csv
- participant_id: P followed by three digits
- name: simulated participant name
- baseline_heart_rate: personal resting reference in beats per minute
- baseline_skin_response: simulated skin-response reference
- baseline_temperature: simulated skin-temperature reference in degrees Celsius
'''
# create a list with the names of the columns for a participant.
PROFILE_COLUMNS = ['participant_id', 'name', 'baseline_heart_rate',
                   'baseline_skin_response', 'baseline_temperature']

'''
fitness_sessions.csv and fitness_sessions_invalid.csv
- session_id: FIT-YYYY-NNN
- participant_id: must exist in participants.csv
- timestamp: non-negative observation index
- heart_rate: beats per minute
- skin_response: simulated non-negative sensor value
- temperature: simulated skin temperature in degrees Celsius
- activity_level: normalized value from 0 to 1
- signal_quality: normalized value from 0 to 1
'''

# create a list with the names of the columns for a session. 
SESSION_COLUMNS = ['session_id', 'participant_id', 'timestamp', 'heart_rate',
                   'skin_response', 'temperature', 'activity_level',
                   'signal_quality']

# Read the rows in the csv files. 
def read_rows(path, expected_columns):
    
    path = Path(path) # call on Path from pathlib

    try: 
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            if header != expected_columns:
                raise DataFileError(f'{path.name}: unexpected header {header}, expected {expected_columns}')
            for row in reader:
                if not row: # skip the blank lines
                    continue
                yield reader.line_num, row

    except FileNotFoundError:
        raise DataFileError(f'{path}: file not found') from None
    
    except PermissionError:
        raise DataFileError(f'{path}: permission denied') from None
    
    except (csv.Error, UnicodeDecodeError) as error:
        raise DataFileError(f'{path}: cannot read the file as a csv ({error})') from error

# We also need to check that the rows has the right number of cells or that they are not empty.
# This is to ensure that the data in the csv is in the correct format. 
def check_row(row, columns):
    if len(row) != len(columns):
        raise InvalidRecordError('row', f' Expected {len(columns)} fields, got {len(row)} fields')
    for column, cell in zip(columns, row):
        if cell.strip() == '':
            raise InvalidRecordError(column, 'missing value')

# We also need to keep track of the rejceted rows. 
# So that the rows that are invalid get stored somewhere. 
def record_rejected(rejected, source, line_number, error):
    rejected.append({
        'source': source,
        'row': line_number,
        'field': error.field,
        'reason': str(error)
    })

# The function load_participant returns the participant ID and the participant info. 
# If its not there, then add it to the rejected.
def load_participants(path, rejected):
    path = Path(path)
    participants = {}

    for line_number, row in read_rows(path, PROFILE_COLUMNS):
        try:
            check_row(row, PROFILE_COLUMNS)
            check_valid_participant_id(row[0].strip())
            participant = Participant.from_row(row)

            if participant.participant_id in participants: # Check if the participant is already in participants.
                raise InvalidRecordError('participant_id', f'Duplicate participant {participant.participant_id}')
            
            participants[participant.participant_id] = participant

        except (InvalidIdentifierError, InvalidRecordError) as error:
            record_rejected(rejected, path.name, line_number, error)

    return participants

# Now we need to load a session.
# Using the same logic as with load_participants. 


def load_sessions(path, participants, rejected, sessions=None):

    path = Path(path)
    if sessions is None:
        sessions = {}
    accepted = 0

    for line_number, row in read_rows(path, SESSION_COLUMNS):
        try:
            check_row(row, SESSION_COLUMNS)
            session_id = check_valid_session_id(row[0].strip())
            participant_id = check_valid_participant_id(row[1].strip())

            if participant_id not in participants: # check if the participant exists. 
                raise InvalidRecordError('participant_id', f' Unknown participant {participant_id}')

            observation = Observation.from_row(row[2:])

            
            # after necessary checks we have ensured that the invalid rows are not with us in the session. 
            session = sessions.get(session_id)

            if session is None:
                session = Session(session_id, participants[participant_id])
                sessions[session_id] = session
            elif session.participant.participant_id != participant_id:
                raise InvalidRecordError('participant_id', f' Session {session_id} already belongs to {session.participant.participant_id}')

            session.add_observation(observation)
            accepted += 1

        except (InvalidIdentifierError, InvalidRecordError) as error: # If the session is not valid, add it to the rejected.
            record_rejected(rejected, path.name, line_number, error)

    return sessions, accepted
