"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from __future__ import annotations
from helpers import cd_to_datetime, datetime_to_str
from typing import Optional, List
import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(
        self,
        designation: str = '',
        name: Optional[str] = None,
        diameter: float = float('nan'),
        hazardous: bool = False,
    ) -> None:
        """Create a new `NearEarthObject`.

        :param designation: A string of the primary designation for this NearEarthObject.
        :param name: A string of the IAU name for this NearEarthObject.
        :param diameter: A float of the diameter, in kilometers, of this NearEarthObject.
        :param hazardous: A boolean whether or not this NearEarthObject is potentially hazardous.
        """
        self.designation: str = designation
        self.name: Optional[str] = name
        self.diameter: float = diameter
        self.hazardous: bool = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches: List[CloseApproach] = []

    @classmethod
    def create(cls, neo_row) -> NearEarthObject:
        return cls(
            designation=str(neo_row[3]),
            name=str(neo_row[4]) if neo_row[4] else None,
            diameter=float(neo_row[15]) if neo_row[15] else float('nan'),
            hazardous=True if str(neo_row[7]) == "Y" else False
        )

    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        _is_hazardous = "is" if self.hazardous else "is not"
        return f"A NearEarthObject named '{self.fullname}' " \
               f"has a diameter of {self.diameter:.3f} km " \
               f"and {_is_hazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(
        self,
        designation: str = '',
        time: Optional[str] = None,
        distance: float = 0.0,
        velocity: float = 0.0,
    ) -> None:
        """Create a new `CloseApproach`.

        :param designation: A string of the primary designation for the NearEarthObject.
        :param time: A string of NASA-formatted calendar date/time, at which the NEO passes closest to Earth.
        :param distance: A float of the nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param velocity: A float of the velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        """
        self._designation: str = designation
        self.time: Optional[datetime.datetime] = cd_to_datetime(time) if time else None
        self.distance: float = distance
        self.velocity: float = velocity

        # Create an attribute for the referenced NEO, originally None.
        self.neo: Optional[NearEarthObject] = None

    @classmethod
    def create(cls, data) -> CloseApproach:
        return cls(
            designation=str(data[0]),
            time=str(data[3]) if data[3] else None,
            distance=float(data[4]) if data[4] else 0.0,
            velocity=float(data[7]) if data[7] else 0.0,
        )

    @property
    def time_str(self) -> str:
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        neo_name = self.neo.fullname if self.neo else self._designation
        return f"On {self.time_str} in UTC, " \
               f"the NEO named '{neo_name}' " \
               f"approaches Earth at a distance of {self.distance:.2f} au " \
               f"with a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
