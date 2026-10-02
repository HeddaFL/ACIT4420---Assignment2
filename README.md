# Python Programming Assignment l

### Course: ACIT4420 - Python Programming Assignment 1
#### Option A: Smart Fitness Session Analyzer 
Student name: Hedda Fløtre Laupstad
Student number: helau2698 

## Description
This program reads the participants and their fitness sessions from csv files. The rows in the csv files are validated and checked against errors/exceptions to ensure that everything is correct. Once the rows are accepted they are group by sessions and connected to the participant (ID). Every session is compared with the participants baseline (heart_reate, skin_response and temperature), classified (resting, moderate, high, recovering or insufficient) and saved into reports. The reports are three different files that can be found in the /output folder (due to me running the code and creating the reports). 

## Project Structure
The repository has the package "analyzer" that contains the program (pipeline) that is used in the program. 

The folder /Assignment_II_Pack contains the data and files provided for the assignment. 

The folder /output contains the generated output from running the program. 

## Class Designs 
The classes used in Assignment2 is the same onces used in Assignment1 in this course. So the logic for assignment2 builds on assignment1. In assignment1, the classes Participant, SensorReading, Observation and Session has three seperate files, in this program these classes are all located inside models.py. 

The four meaningful classes are: Participant, SensorReading (abstract), Observation and Session. 

Class Participant: 
- Stores one participants identifier and personal baseline values (heart rate, skin response, temperature).
- The classmethod "from_row" builds a Participant from one row of participants.csv. 

Class SensorReading: 
- An abstract base class using ABC. 
- It shores a timestamp, tracks validation errors and exposes an "is_valid" property. 
- It also declears an abstract "validate()" method that subclasses must implement. 

Class Observation: 
- is a subclass of SensorReading.
- represents one measurement window (heart rate, skin response, temperature, activity level, signal quality).
- implements the method "validate()" to check each field against a range. 
- adds a "is_usable" property where a valid observation is signal_quality >= 0.5. This number is to ensure that the sessions have quality. 
- "from_rows" converts the csv rows into numbers and raises InvalidRecorderror if the row is not valid.  

Class Session: 
- represents one traning session for one Participant and many Observation objects. 
- observation list is private.
- exposes usable/rejected observations and counts.
- add_observation() adds the valid observations. 

## Composition, Encapsulation, Inheritance and Overriding
This is the same logic as in assignment1 and has not really changed. 

Composition:
- The class Session contains one Participant and multiple Observation objects. An important note here, is that a Session cannot exist without a Participant, but a Participant can exist without a Session. The relationship is defined by a "has-a". Composition is therefore a natural choice for the class.

Encapsulation: 
- All classes use private attributes (__ prefix) and properties (@property). This ensures that a participants Id and baseline values cannot be changed or reassigned by accident. 
- Another encapsulation is that Session returns a copy of its observation list. This ensures that the real observation list cannot be changed. The way to add data is through "add_observation()".

Inheritance: 
- The class Observation inherits from the abstract class SensorReading. This means that the parent (SensorReading) defines what each and every sensor reading needs, while the child class (Observation) defines what a fitness observation should measure and how to valide it. This relationship ensures that the parent class gives a minimum level of values while a child class can be more specific. The use of SensorReading as parent and Observation as child classes is because of the "is-a" relationship. An Observation is a type of SensorReading. This choice helps me avoid duplicating common behavior observed.

Overriding: 
- The class Observation implements the abstract validate() method, which is defined by the class SensorReading. It is not instantiated in SensorReading, which means that every subclass of SensorReading need to define and valide its own rules insted of inheriting. 

## Running instructions

```
git clone XXXXXXXXXXXXXXxxxxx
cd XXXXXXXXXxxxx
python main.py --profiles Assignment_II_Pack/data/option_a_fitness/participants.csv --sessions Assignment_II_Pack/data/option_a_fitness/fitness_sessions.csv Assignment_II_Pack/data/option_a_fitness/fitness_sessions_invalid.csv --output output
```

## Example output from main.py
Output in the terminal:
```
Accepted rows: 33
Rejected rows: 10
Sessions analyzed: 6
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

The output of file rejected_record.txt
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
- test_boundary_heart_rate (checks that if heart_rate is our of bound that it it is rejected, it is manually set to ensure that the hart_rate is out of bounds)

To run the test in tests.py use the following command:

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

The session where every row is rejected is not in the summary, but in the "rejected_record.txt".

The thresholds i used for the attributes (for instance 45 in max heart rate difference) are chosen by me based on the small dataset provided. This means that different data or bigger data might make a session be classified differently. 