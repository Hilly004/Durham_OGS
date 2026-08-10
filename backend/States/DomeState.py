from enum import Enum

class DomePosition(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSED = 2
    PARTIALLY_OPEN = 3

class DomeMotion(Enum):
    IDLE = 0
    OPENING = 1
    CLSOING = 2
    STOPPING = 3
    UNKNOWN = 4

class DomeState:
    connected: bool
    fault: bool

    position: DomePosition
    motion: DomeMotion

    left_angle: float
    right_angle: float
    