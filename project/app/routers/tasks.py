from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Security

from project.auth import get_current_user
from project.background_tasks import send_email
from project.db import SessionDep, get_users_by_id
from project.db_models import Task, User
from project.models import TaskData, TaskStatus

router = APIRouter()


@router.post("/tasks/")
async def create_task(
    task: TaskData,
    current_user: Annotated[User, Security(get_current_user, scopes=["manager"])],
    session: SessionDep,
) -> Task:
    task_dict = task.model_dump()
    task_dict.update(
        {
            "responsible": current_user,
            "performers": get_users_by_id(session, task_dict.pop("performers")),
        }
    )
    db_task = Task(**task_dict)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.post("/tasks/{task_id}/")
async def update_task_status(
    task_id: int,
    body: TaskStatus,
    current_user: Annotated[User, Security(get_current_user, scopes=["performer"])],
    session: SessionDep,
    background_tasks: BackgroundTasks,
) -> Task:
    db_task = session.get(Task, task_id)
    db_task.status = body.status
    session.commit()
    session.refresh(db_task)
    background_tasks.add_task(
        send_email,
        email_address=db_task.responsible.email,
        message=f"{db_task.title} task status was changed to {body.status}",
    )
    return db_task
