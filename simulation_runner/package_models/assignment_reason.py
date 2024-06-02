from enum import Enum


class AssignmentReason(Enum):
    ORDINARY = 0  # This is for ordinary passengers, no reporting or express
    EXPRESS = 1  # This is for reporting passengers that are assigned to an express bus
    ORDINARY_IS_FASTER = 2  # This is for reporting passengers that are assigned to an ordinary bus because it is faster
    LUCKY_EXPRESS_REPORTING = 3  # This is for late reporting passengers that are assigned to an express bus because they are lucky
    LUCKY_ORDINARY_IS_FASTER = 4  # This is for late reporting passengers that are assigned to an ordinary bus because it is faster, although they are lucky
    LATE_REPORT_EXPRESS = 5  # This is for late reporting passengers that are assigned to the next express bus because it is faster
    LATE_REPORT = 6  # This is for late reporting passengers that are assigned to an ordinary bus because they are late
