# Python Programming Assignment 2

### Course: ACIT4420 - Python Programming Assignment 2
#### Option A: Smart Fitness Session Analyzer 
##### Student name: Hedda Fløtre Laupstad
##### Student number: helau2698 

## Description
This program reads the participants and their fitness sessions from csv files. The rows in the csv files are validated and checked against errors/exceptions to ensure that everything is correct. Once the rows are accepted they are group by sessions and connected to the participant (ID). Every session is compared with the participants baseline (heart_rate, skin_response and temperature), classified (resting, moderate, high, recovering or insufficient) and saved into reports. The reports are three different files that can be found in the /output folder (due to me running the code and creating the reports). 

## Project Structure
The repository has the package "analyzer" that contains the program (pipeline) that is used in the program. Inside the package is these files:
- analysis.py 
- errors.py
- loader.py
- models.py
- reports.py
- validators.py

The folder /Assignment_II_Pack contains the data and files provided for the assignment. 

The folder /output contains the generated output from when i ran the program. 

The files main.py and tests.py are in the root folder. 

## Class Designs 
The classes used in Assignment2 is the same onces used in Assignment1 in this course. So the logic for assignment2 builds on assignment1. In assignment1, the classes Participant, SensorReading, Observation and Session has three seperate files, in this program these classes are all located inside models.py.

## Composition, Encapsulation, Inheritance and Overriding
This assignment builds on assignment1 and thus uses the same composition, encapsulation, inheritance and overriding. 

Composition:
- Session contains one Participant and multiple Observation objects. 
- A Session cannot exist without a Participant, but a Participant can exist without a Session. The relationship is a "has-a".

Encapsulation: 
- Participant, Observation and Session use private attributes (__ prefix) and properties (@property). Ensures that IDs and baselines cannot be changed.  
- Session returns a copy of its observation list, ensuring that observations cannot be changed. 

Inheritance: 
- Observation inherits from the abstract class SensorReading. 
- The use of SensorReading as parent and Observation as child classes is because of the "is-a" relationship. 
- An Observation is a type of SensorReading.

Overriding: 
- Observation implements the abstract validate() method, which is defined by the class SensorReading. 
- Meaning that every child need to define a validate() method for their own.  

## Validation and error/exception 
The identifiers are validated with regular expressions and "fullmatch". I used the regular expressions from the assignment text: 
- Participant ID: ^P\d{3}$
- Fitness session ID: ^FIT-\d{4}-\d{3}$

Additionally i have some set value ranges in the program, these are:
- heart_rate: 35 to 205 (outside of the range is not plausable)
- timestamp: >= 0 (set as 'inf') (described in DATA_DICTIONARY.txt as non-negative)
- skin_response: >= 0 (set as 'inf') (described in DATA_DICTIONARY.txt as non-negative)
- temperature: 25 to 42 (data shows 32-34, so plausable skin temperature)
- activity_level: 0.0 to 1.0 (set by DATA_DICTIONARY.txt)
- signal_quality: 0.0 to 1.0 (set by DATA_DICTIONARY.txt)

The reasoning behind each value is different, where some of them where set inside the file DATA_DICTIONARY.txt and some where set by me to ensure that only valid and possible data is used. 

Rows can be rejected if they are not inside of the ranges, but they can also be rejected if:
- wrong number of fields
- empty field
- value cannot convert to a number
- participant ID is not in participants.csv
- session belongs to another participant
- duplicate participant IDs are rejected

In the file errors.py i created some errors(exceptions) that i could use to handle errors and raise exceptions. These are: 
- InvalidIdentifierError: raise an error if an ID is invalid in format.
- InvalidRecordError: raise an error if a row value is misisng, wrong value or is out of range.
- DataFileError: raise an error if a file is not found, no permission, wrong header or cannot write output.

(InvalidRecordError and InvalidIdentifierError where mentioned in the assignment text under 4.4 Handle errors)

The program accomodates that the session should continue safely when possible by raising errors/exceptions, these are:
- bad rows are added to the rejected list with information. 
- missing or unreadable profile files stops the program, becuase there is no session to be checked without a partctpant. 
- missing or unreadable sessions are skipped.  

It was also mentioned in the assignment text to handle FileNotFoundError, PermissionError, ValueError, KeyError and csv errors where they may occur. To ensure that the erros are caught, i have used file errors and csv erros in the function read_rows(), ValueError in the functions to_int() and to_float() and KeyError is not used due to every participant being lookedup by an in check. 

## Classifications and Assumptions
I used the same classification rules from assignment1 into assignment2. These are: resting, moderate activity, high activity, recovering and insufficient data. 

The rules used for the classification is in the described order below:
- Less than 3 usable observations gives insufficient data.
- At least 4 usable observtaions for recovery. They are split in two and sorted by timestamp. The Mean heart rate of the second half is more than 3 bpm lower than in the first half, and the mean activity of the second half is more than 0.05 lower than in the first half.  
- Mean activity < 0.25 and mean heart rate less than 12 bpm above baseline gives resting classification. 
- Mean activity < 0.68 and mean heart rate less than 45 bpm above baseline gives moderate activity classification.
- Else it is high activity. 
- For signal quality is an observation only usable if it is valid and higher or equal to 0.5. A low-quality observation is counted but left out of the statistics. 

The reasoning behind the classification is my own reasoning based on the provided small data set. Due to the order of rules this means that the first rule that is checked and accepted is used. 

(I have used the same set numbers for assignment2 as in assignment1. So this means a lot of the assumptions are the same.) 

## Running instructions
Only standard python library is needed to run the program. Use the following commands to run:
```
git clone https://github.com/HeddaFL/ACIT4420---Assignment2.git
cd ACIT4420---Assignment2
python main.py --profiles Assignment_II_Pack/data/option_a_fitness/participants.csv --sessions Assignment_II_Pack/data/option_a_fitness/fitness_sessions.csv Assignment_II_Pack/data/option_a_fitness/fitness_sessions_invalid.csv --output output
```
The program creates the folder /output. If it does not exist, the three files are created inside the folder. If the folder exists from before, the three files overwrite the previous ones each time.  

## Example output from main.py
Output in the terminal:
```
Accepted rows: 33
The 33 accepted rows are made up of 3 participants and 30 session rows.
Rejected rows: 10
Sessions analyzed: 6
Participants: 3
Created files:
 - output\analysis_summary.csv
 - output\analysis_report.txt
 - output\rejected_records.txt
```

The output of file analysis_report.txt
```
===================================================================
Session FIT-2026-001 with Amina Noor (P001)
===================================================================
Classification: RESTING
Reason: mean heart rate 68.8 bpm is +0.8 vs baseline 68, mean activity 0.09
Observations used: 6 of 6 (0 excluded because of low signal quality)
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
-------------------------------------------------------------------
  Heart rate     : average 68.83 bpm (min 68, max 70, n=6), +0.83 vs baseline
  Skin response  : average 1.19 (min 1.17, max 1.22, n=6), -0.01 vs baseline
  Temperature    : average 32.43 C (min 32.4, max 32.5, n=6), +0.03 vs baseline
  Activity level : average 0.09 (min 0.07, max 0.12, n=6)

===================================================================
Session FIT-2026-002 with Jonas Berg (P002)
===================================================================
Classification: MODERATE ACTIVITY
Reason: mean heart rate 102.0 bpm is +28.0 vs baseline 74, mean activity 0.49
Observations used: 6 of 6 (0 excluded because of low signal quality)
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
-------------------------------------------------------------------
  Heart rate     : average 102 bpm (min 78, max 118, n=6), +28.00 vs baseline
  Skin response  : average 2.01 (min 1.55, max 2.4, n=6), +0.56 vs baseline
  Temperature    : average 33.13 C (min 32.8, max 33.4, n=6), +0.43 vs baseline
  Activity level : average 0.49 (min 0.22, max 0.68, n=6)

===================================================================
Session FIT-2026-003 with Maya Chen (P003)
===================================================================
Classification: HIGH ACTIVITY
Reason: mean heart rate 132.5 bpm is +69.5 vs baseline 63, mean activity 0.75
Observations used: 6 of 6 (0 excluded because of low signal quality)
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
-------------------------------------------------------------------
  Heart rate     : average 132.5 bpm (min 72, max 162, n=6), +69.50 vs baseline
  Skin response  : average 3.24 (min 1.3, max 4.2, n=6), +2.14 vs baseline
  Temperature    : average 33.53 C (min 32.5, max 34.1, n=6), +1.23 vs baseline
  Activity level : average 0.75 (min 0.25, max 0.94, n=6)

===================================================================
Session FIT-2026-004 with Amina Noor (P001)
===================================================================
Classification: RECOVERING
Reason: Heart rate fell from 120.3 to 106.0 bpm and activity fell from 0.66 to 0.43 over the second half of the session
Observations used: 6 of 6 (0 excluded because of low signal quality)
Recovery detected: yes - Heart rate fell from 120.3 to 106.0 bpm and activity fell from 0.66 to 0.43 over the second half of the session
-------------------------------------------------------------------
  Heart rate     : average 113.17 bpm (min 72, max 151, n=6), +45.17 vs baseline
  Skin response  : average 2.58 (min 1.35, max 3.9, n=6), +1.38 vs baseline
  Temperature    : average 33.28 C (min 32.6, max 33.9, n=6), +0.88 vs baseline
  Activity level : average 0.55 (min 0.18, max 0.92, n=6)

===================================================================
Session FIT-2026-005 with Jonas Berg (P002)
===================================================================
Classification: INSUFFICIENT DATA
Reason: only 0 of 5 observations have signal_quality >= 0.5; at least 3 are needed
Observations used: 0 of 5 (5 excluded because of low signal quality)
Recovery detected: no - Not enough usable observations to evaluate recovery. There is (0), but we need at least 4
-------------------------------------------------------------------
  Heart rate     : no usable data
  Skin response  : no usable data
  Temperature    : no usable data
  Activity level : no usable data

===================================================================
Session FIT-2026-101 with Amina Noor (P001)
===================================================================
Classification: INSUFFICIENT DATA
Reason: only 1 of 1 observations have signal_quality >= 0.5; at least 3 are needed
Observations used: 1 of 1 (0 excluded because of low signal quality)
Recovery detected: no - Not enough usable observations to evaluate recovery. There is (1), but we need at least 4
-------------------------------------------------------------------
  Heart rate     : average 72 bpm (min 72, max 72, n=1), +4.00 vs baseline
  Skin response  : average 1.3 (min 1.3, max 1.3, n=1), +0.10 vs baseline
  Temperature    : average 32.5 C (min 32.5, max 32.5, n=1), +0.10 vs baseline
  Activity level : average 0.1 (min 0.1, max 0.1, n=1)

```

The output of file analysis_summary.csv
```
session_id,participant_id,participant_name,total_observations,usable_observations,low_quality_observations,mean_heart_rate,mean_skin_response,mean_temperature,mean_activity_level,heart_rate_vs_baseline,skin_response_vs_baseline,temperature_vs_baseline,classification,classification_reason,recovery_detected
FIT-2026-001,P001,Amina Noor,6,6,0,68.83,1.19,32.43,0.09,0.83,-0.01,0.03,resting,"mean heart rate 68.8 bpm is +0.8 vs baseline 68, mean activity 0.09",False
FIT-2026-002,P002,Jonas Berg,6,6,0,102,2.01,33.13,0.49,28,0.56,0.43,moderate activity,"mean heart rate 102.0 bpm is +28.0 vs baseline 74, mean activity 0.49",False
FIT-2026-003,P003,Maya Chen,6,6,0,132.5,3.24,33.53,0.75,69.5,2.14,1.23,high activity,"mean heart rate 132.5 bpm is +69.5 vs baseline 63, mean activity 0.75",False
FIT-2026-004,P001,Amina Noor,6,6,0,113.17,2.58,33.28,0.55,45.17,1.38,0.88,recovering,Heart rate fell from 120.3 to 106.0 bpm and activity fell from 0.66 to 0.43 over the second half of the session,True
FIT-2026-005,P002,Jonas Berg,5,0,5,,,,,,,,insufficient data,only 0 of 5 observations have signal_quality >= 0.5; at least 3 are needed,False
FIT-2026-101,P001,Amina Noor,1,1,0,72,1.3,32.5,0.1,4,0.1,0.1,insufficient data,only 1 of 1 observations have signal_quality >= 0.5; at least 3 are needed,False

```

The output of file rejected_records.txt
```
fitness_sessions_invalid.csv line 3 [heart_rate]: Invalid Record: (heart_rate:Cannot convert 'fast' into int value.)
fitness_sessions_invalid.csv line 4 [participant_id]: Invalid Identifier: (participant_id:'001')
fitness_sessions_invalid.csv line 5 [activity_level]: Invalid Record: (activity_level:missing value)
fitness_sessions_invalid.csv line 6 [signal_quality]: Invalid Record: (signal_quality:1.4 is outside of the range (0.0 to 1.0))
fitness_sessions_invalid.csv line 7 [session_id]: Invalid Identifier: (session_id:'FIT-26-102')
fitness_sessions_invalid.csv line 8 [participant_id]: Invalid Record: (participant_id: Unknown participant P999)
fitness_sessions_invalid.csv line 9 [timestamp]: Invalid Record: (timestamp:Cannot convert 'two' into int value.)
fitness_sessions_invalid.csv line 10 [heart_rate]: Invalid Record: (heart_rate:-15 is outside of the range (35 to 205))
fitness_sessions_invalid.csv line 11 [skin_response]: Invalid Record: (skin_response:-0.5 is outside of the range (0.0 to inf))
fitness_sessions_invalid.csv line 12 [row]: Invalid Record: (row: Expected 8 fields, got 7 fields)

```

## Testing
The file tests.py uses unittest and the provided csv files with valid and invalid data. The file has four functions:
- test_valid_file (checks only valid data, used as a control/baseline)
- test_invalid_file (checks invalid data)
- test_missing_file (checks that a file that do not exist will raise an error/exception, it is manually set with a file that do not exist)
- test_boundary_heart_rate (checks that if heart_rate is out of bound that it is rejected, it is manually set to ensure that the heart_rate is out of bounds)

The test.py should be run from the repository root.
To run tests.py use the following command:

``` 
python -m unittest tests -v 
```

## Example output from tests.py
```
test_boundary_heart_rate (tests.TestProgram.test_boundary_heart_rate) ... ok
test_invalid_file (tests.TestProgram.test_invalid_file) ...ok
test_missing_file (tests.TestProgram.test_missing_file) ...ok
test_valid_file (tests.TestProgram.test_valid_file) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.008s

OK
```

## Known limitations
One known limitation is that when the rows are checked, only the first invalid reason is listed. This means that if a row has more than one invalid cell, the program will not give a reason for both, only the first one. 

The session where every row is rejected is not in the summary, but in the "rejected_records.txt".

The thresholds i used for the attributes (for instance 45 in max heart rate difference) are chosen by me based on the small dataset provided. This means that different data or bigger data might make a session be classified differently.

The recovery classification is checked before activity rules so a session could end calmer than it started. Meaning that a session could be classified as recovering even if the mean heart rate is high. 

The participants baselines are not range checked from participants.csv. 

A session that is classified as insufficient data could still show baseline differences because it was from a single reading. 
