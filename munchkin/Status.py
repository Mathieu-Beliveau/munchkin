from enum import Enum


class Status(Enum):
    RUNNING = 1,
    PAUSED = 2,
    CONNECTION_LOST = 3
