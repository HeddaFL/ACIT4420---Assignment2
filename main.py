"""
Purpose: connect all of the modules (files) and help run the command line to get the output.
"""

# imports
import argparse
import sys
from analyzer.analysis import generate_session_summary
from analyzer.errors import DataFileError
from analyzer.loader import load_participants, load_sessions
from analyzer.reports import write_outputs
 
# help read the command line arguments used when running main.py
def parse_args(argv=None):
    parser = argparse.ArgumentParser(description = 'Smart Fitness Session Analyzer')
    parser.add_argument('--profiles', required = True,
                        help = 'csv file with the participants, for example data/participants.csv')
    parser.add_argument('--sessions', required = True, nargs = '+',
                        help = 'one or more csv files with sessions, for example data/fitness_sessions.csv')
    parser.add_argument('--output', default = 'output',
                        help = 'folder for the output files (created if it does not exist)')
    return parser.parse_args(argv)
 
# Run the pipeline (the package) and return 0 if its done and 1 if it had to stop. 
def main(argv=None):
    args = parse_args(argv)
    rejected = []   # shared list: the loader adds every rejected row to it
 
    # Without the participants nothing can be checked, so a problem here stops the program.
    try:
        participants = load_participants(args.profiles, rejected)
    except DataFileError as error:
        print(f'Cannot continue: {error}', file=sys.stderr)
        return 1
 
    # A problem with one session file should not stop the others.
    sessions = {}
    accepted_session_rows = 0
    files_read = 0
    for path in args.sessions:
        try:
            sessions, accepted = load_sessions(path, participants, rejected, sessions)
        except DataFileError as error:
            print(f'Skipping session file: {error}', file=sys.stderr)
            continue
        accepted_session_rows += accepted
        files_read += 1
 
    if files_read == 0:
        print('Cannot continue: none of the session files could be read.', file=sys.stderr)
        return 1
 
    results = [generate_session_summary(session) for session in sessions.values()]
 
    try:
        created_files = write_outputs(args.output, results, rejected)
    except DataFileError as error:
        print(f'Cannot write the output files: {error}', file=sys.stderr)
        return 1
 
    # To verify that the completion is done, 
    # the terminal should display the number of accepted, rejected, sessions analyzed 
    # and the names of the files created. 
    print(f'Accepted rows: {len(participants) + accepted_session_rows}')
    print(f'The {len(participants) + accepted_session_rows} accepted rows are made up of {len(participants)} participants and {accepted_session_rows} session rows.')
    print(f'Rejected rows: {len(rejected)}')
    print(f'Sessions analyzed: {len(results)}')
    print('Created files:')
    for file in created_files:
        print(f' - {file}')
    return 0
 
 
if __name__ == '__main__':
    sys.exit(main())

