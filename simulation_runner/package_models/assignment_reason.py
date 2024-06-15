from enum import Enum


class AssignmentReason(Enum):
    ORDINARY = 0  # This is for ordinary passengers that are assigned to an ordinary bus and it is the next one
    ORDINARY_REJECTED = 1  # This is for ordinary passengers that are rejected (next bus is express and they cannot abaord it)
    EXPRESS = 2  # This is for reporting passengers that are assigned to an express bus
    ORDINARY_IS_FASTER = 3  # This is for reporting passengers that are assigned to an ordinary bus because it is faster
    LUCKY_EXPRESS_REPORTING = 4  # This is for late reporting passengers that are assigned to an express bus because they are lucky
    LUCKY_ORDINARY_IS_FASTER = 5  # This is for late reporting passengers that are assigned to an ordinary bus because it is faster, although they are lucky
    LATE_REPORT_EXPRESS = 6  # This is for late reporting passengers that are assigned to the next express bus because it is faster
    LATE_REPORT = 7  # This is for late reporting passengers that are assigned to an ordinary bus because they are late
    NO_BUS = 8  # This is for passengers that are not assigned to any bus because there is no bus for them (most likely because out of simulation time)
