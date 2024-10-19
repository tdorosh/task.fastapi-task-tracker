from pydantic import BaseModel

from project.enums import TaskPriorityEnum, TaskStatusEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class TaskData(BaseModel):
    title: str
    description: str
    priority: TaskPriorityEnum
    performers: list[int]


class TaskStatus(BaseModel):
    status: TaskStatusEnum
