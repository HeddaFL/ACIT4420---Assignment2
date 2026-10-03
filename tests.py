"""
Purpose: To check that the program works as intended on valid and invalid data.
As well as missing files and boundary cases.
"""

# imports
import unittest
from pathlib import Path

from analyzer.errors import DataFileError, InvalidRecordError
from analyzer.loader import load_participants, load_sessions
from analyzer.validators import HEART_RATE_RANGE, range_check

# the path to find the data csv files. 
DATA_DIR = Path("Assignment_II_Pack/data/option_a_fitness")

# Create a class to test the loader and validators. 
class TestProgram(unittest.TestCase):

    def setUp(self):
        self.rejected = []
        self.people = load_participants(DATA_DIR / "participants.csv", self.rejected)

    # Control that the valid data is accepted without rejected rows. 
    # Used as a control/baseline, to check if the program works with valid and invalid data. 
    def test_valid_file(self):
        sessions, accepted = load_sessions(DATA_DIR / "fitness_sessions.csv",
                                           self.people, self.rejected)
        self.assertEqual(accepted, 29)
        self.assertEqual(len(sessions), 5)
        self.assertEqual(self.rejected, [])

    # Use purposeful invalid data to ensure that the program catches it. 
    def test_invalid_file(self):
        _, accepted = load_sessions(DATA_DIR / "fitness_sessions_invalid.csv",
                                           self.people, self.rejected)
        self.assertEqual(accepted, 1)
        self.assertEqual(len(self.rejected), 10)
        self.assertEqual(self.rejected[1]["row"], 4)
        self.assertEqual(self.rejected[1]["field"], "participant_id")

    # Check that a file that do not exist raises DataFileError.
    def test_missing_file(self):
        with self.assertRaises(DataFileError):
            load_sessions(DATA_DIR / "test_do_not_exist.csv", self.people, self.rejected)

    # Boundary test for heart_rate only. 
    def test_boundary_heart_rate(self):
        low, high = HEART_RATE_RANGE # reminder: current range of heart_rate is 35 to 205, defined in validators.py. 
        self.assertEqual(range_check("heart_rate", low, low, high), low) 
        with self.assertRaises(InvalidRecordError):
            range_check("heart_rate", low - 1, low, high) # make the heart_rate out of bound by having the value be below the lowest allowed value.


if __name__ == "__main__":
    unittest.main()