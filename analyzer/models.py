"""
Purpose: objects that represent the data through classes: 
- Participant
- Observation
- SensorReading (abstract)
- Session

I have reused the structure and some of the code of the classes from Assignment 1. 
"""

# imports
from abc import ABC, abstractmethod
from .errors import InvalidRecordError
from .validators import (to_int, to_float, range_check, HEART_RATE_RANGE,
                         TEMPERATURE_RANGE, ACTIVITY_LEVEL_RANGE,
                         SIGNAL_QUALITY_RANGE, SKIN_RESPONSE_RANGE,
                         TIMESTAMP_RANGE)

# readings with a signal_quality below this are poor quality and excluded from the analysis
MIN_SIGNAL_QUALITY = 0.5


class Participant:
    # Represent a participant and their personal baseline measurements.

    # CHANGED: add name, since participants.csv has column named 'name'.
    def __init__(
        self, 
        participant_id, 
        name, 
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature):

        if not isinstance(participant_id, str) or not participant_id.strip():
            raise ValueError("participant_id must be a non-empty string")

        # create .__ private attributes.
        self.__participant_id = participant_id
        self.__name = name
        self.__baseline_heart_rate = baseline_heart_rate
        self.__baseline_skin_response = baseline_skin_response
        self.__baseline_temperature = baseline_temperature

    # use @ to create properties. 
    @property
    def participant_id(self):
        # return the participant identifier
        return self.__participant_id

    @property 
    def name(self):
        # return the participant name
        return self.__name

    @property
    def baseline_heart_rate(self):
        # return the baseline heart rate
        return self.__baseline_heart_rate

    @property
    def baseline_skin_response(self):
        # return the baseline skin response
        return self.__baseline_skin_response

    @property
    def baseline_temperature(self):
        # return the baseline temperature
        return self.__baseline_temperature

    # CHANGED:the function from_row is different in this assignment than in Assignment 1. 
    # This is due to the data coming from different places.
    @classmethod
    def from_row(cls, cells):
        # Create a Participant from the columns in participants.csv.
        # Convert generated csv data into a Participant object.

        return cls(
            participant_id = cells[0].strip(),
            name = cells[1].strip(),
            baseline_heart_rate = to_int("baseline_heart_rate", cells[2]),
            baseline_skin_response = to_float("baseline_skin_response", cells[3]),
            baseline_temperature = to_float("baseline_temperature", cells[4])
        )

    def __str__(self):
        return (f"Participant: ({self.participant_id}, {self.name}, "
                f"Heart Rate = {self.baseline_heart_rate}, "
                f"Skin Response = {self.baseline_skin_response}, "
                f"Temperature = {self.baseline_temperature})")

    # if two participants have the same ID they should be treated as identity, not baseline values.
    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return (
            self.__participant_id == other.__participant_id)

    # defining __eq__ removes Python's default hash, so it is defined again from the ID.
    def __hash__(self):
        return hash(self.__participant_id)
    


# Class SensorReading is based on Assignment 1.
# CHANGED: the timestamp is stored once here and exposed as a read-only property.
class SensorReading(ABC):
    # Abstract class that Observation can inherit from.

    def __init__(self, timestamp):
        self._timestamp = timestamp
        self._validation_errors = []

    @property
    def timestamp(self):
        return self._timestamp

    # CHANGED: each validation error is a (field, reason) pair. A copy is returned
    # so that no one can change the list from outside.
    @property
    def validation_errors(self):
        return list(self._validation_errors)

    @property
    def is_valid(self):
        return len(self._validation_errors) == 0

    # ensure that validate() will raise an error. 
    @abstractmethod
    def validate(self):
        raise NotImplementedError("ERROR: validate method not implemented.")


class Observation(SensorReading):
    # Measurement observation window. 

    def __init__(
            self, 
            timestamp,
            heart_rate,
            skin_response,
            temperature,
            activity_level,
            signal_quality,):

        super().__init__(timestamp)

        # private attributes, read through the properties below.
        # (the timestamp is stored in SensorReading)
        self.__heart_rate = heart_rate
        self.__skin_response = skin_response
        self.__temperature = temperature
        self.__activity_level = activity_level
        self.__signal_quality = signal_quality
        self.validate()

    # use @ to create properties, same as in Participant.
    @property
    def heart_rate(self):
        return self.__heart_rate

    @property
    def skin_response(self):
        return self.__skin_response

    @property
    def temperature(self):
        return self.__temperature

    @property
    def activity_level(self):
        return self.__activity_level

    @property
    def signal_quality(self):
        return self.__signal_quality

    # validate() checks if the fields are valid.
    # CHANGED: it uses range_check and the ranges from validators.py, so the limits
    # are defined in one place. Each failure is stored as a (field, reason) pair.
    def validate(self):
        self._validation_errors = []

        checks = (
            ("timestamp", self.timestamp, TIMESTAMP_RANGE),
            ("heart_rate", self.heart_rate, HEART_RATE_RANGE),
            ("skin_response", self.skin_response, SKIN_RESPONSE_RANGE),
            ("temperature", self.temperature, TEMPERATURE_RANGE),
            ("activity_level", self.activity_level, ACTIVITY_LEVEL_RANGE),
            ("signal_quality", self.signal_quality, SIGNAL_QUALITY_RANGE),
        )

        for field, value, (low, high) in checks:
            # If there is any None fields it is rejected here, since range_check cannot compare None.
            if value is None:
                self._validation_errors.append((field, "missing value"))
                continue
            try:
                range_check(field, value, low, high)
            except InvalidRecordError as error:
                self._validation_errors.append((field, error.reason))

    # ensure that usable observations is valid and within the signal_quality standard.
    @property
    def is_usable(self):
        return self.is_valid and self.signal_quality >= MIN_SIGNAL_QUALITY

    # CHANGED: the function from_row is different in this assignment than in Assignment 1. 
    # This is due to the data coming from different places.
    @classmethod
    def from_row(cls, cells):
        # Create an Observation from cells in the csv data. 
        # The cells are the columns. 
        
        observation = cls(
            to_int("timestamp", cells[0]),
            to_int("heart_rate", cells[1]),
            to_float("skin_response", cells[2]),
            to_float("temperature", cells[3]),
            to_float("activity_level", cells[4]),
            to_float("signal_quality", cells[5]),
        )

        # an invalid observation is rejected here, so the loader only needs to catch InvalidRecordError.
        # Only the first problem is reported for the row.
        if not observation.is_valid:
            field, reason = observation.validation_errors[0]
            raise InvalidRecordError(field, reason)
        return observation


# holds one participant and a list of observations
class Session:
    # Represent one session for one participant. 

    def __init__(self, session_id, participant):

        if not isinstance(participant, Participant):
            raise TypeError("participant must be a Participant object")
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")
        
        # use .__ to create private attributes.
        self.__session_id = session_id
        self.__participant = participant
        self.__observations = []

    def add_observation(self, observation):
        # Add an Observation object to the session. 

        if not isinstance(observation, Observation):
            raise TypeError("observation must be an Observation object")
        self.__observations.append(observation)
    
    # use @property to create a property. 
    @property 
    def session_id(self):
        return self.__session_id

    @property
    def participant(self):
        return self.__participant

    # ensure no one can modify the observations list directly, only through add_observation
    @property 
    def observations(self):
        return list(self.__observations)  # Return a copy to prevent external modification

    @property
    def usable_observations(self):
        return [obs for obs in self.__observations if obs.is_usable] 

    # observations that are valid but not usable (signal_quality below MIN_SIGNAL_QUALITY).
    # Invalid rows are rejected by Observation.from_row and never enter a session.
    @property
    def low_quality_observations(self):
        return [obs for obs in self.__observations if not obs.is_usable]

    def total_count(self):
        return len(self.__observations) # return the total number of observations.

    def usable_count(self):
        return len(self.usable_observations) # return the total usable observations.

    def low_quality_count(self):
        return len(self.low_quality_observations) # return the number of low-quality observations.

    def __len__(self):
        return len(self.__observations)

    # convert a Session into a string using __str__. 
    def __str__(self): # magic method. 
        return (f"Session ID {self.__session_id} for {self.__participant.participant_id}"
                f" ({self.usable_count()}/{self.total_count()} usable observations)")