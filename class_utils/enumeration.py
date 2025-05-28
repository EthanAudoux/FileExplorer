
# create an enumeration

from enum import Enum

class ModeCreationFile(Enum):
    NONE = 0
    FILE = 1
    DIR = 2
    UNKNOWN = 3
    

class ModeOnOff(Enum):
    ON = 0
    OFF = 1
    
class SortFile(Enum):
    NAME = "By name"
    DATE = "By date"
    SIZE = "By size"
    TYPE = "By type"