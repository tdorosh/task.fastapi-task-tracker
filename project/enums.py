from enum import StrEnum, auto


class TaskStatusEnum(StrEnum):
    todo = auto()
    in_progress = auto()
    done = auto()


class TaskPriorityEnum(StrEnum):
    low = auto()
    medium = auto()
    high = auto()
