from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from project.enums import TaskPriorityEnum, TaskStatusEnum


class UserTaskLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    task_id: int | None = Field(default=None, foreign_key="task.id", primary_key=True)


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    description: str
    users: list["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: EmailStr = Field(index=True)
    password: str
    role_id: int | None = Field(default=None, foreign_key="role.id")
    role: Role | None = Relationship(back_populates="users")
    tasks_to_manage: list["Task"] = Relationship(back_populates="responsible")
    tasks_to_complete: list["Task"] = Relationship(
        back_populates="performers", link_model=UserTaskLink
    )


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    status: TaskStatusEnum = Field(default=TaskStatusEnum.todo)
    priority: TaskPriorityEnum
    responsible_id: int | None = Field(default=None, foreign_key="user.id")
    responsible: User | None = Relationship(back_populates="tasks_to_manage")
    performers: list[User] = Relationship(
        back_populates="tasks_to_complete", link_model=UserTaskLink
    )
