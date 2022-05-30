from enum import Enum


class CarStatus(Enum):
    NEW = 'new'
    CHECK_ENGINE = 'check-engine'
    NORMAL = 'normal'
    TOTALED = 'totaled'
    PASSENGER_DEAD = 'passenger-dead'


class JobStatus(Enum):
    IN_PROGRESS = 'in-progress'
    WAITING = 'waiting'
    NONE = 'none'
