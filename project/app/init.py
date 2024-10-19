import json

from sqlmodel import Session, select

from project.db import create_db_user, engine, get_users_by_id
from project.db_models import Role, Task, User


def setup_initial_data():
    with Session(engine) as session:
        roles_exist = session.exec(select(Role)).first() is not None
        users_exist = session.exec(select(User)).first() is not None

        if not roles_exist and not users_exist:
            with open("fixtures.json") as f:
                fixtures = json.load(f)

            for role in fixtures["roles"]:
                role = Role(title=role["title"], description=role["description"])
                session.add(role)

            for user in fixtures["users"]:
                role = session.exec(
                    select(Role).where(Role.title == user["role"])
                ).first()
                user = create_db_user(
                    name=user["name"],
                    email=user["email"],
                    password=user["password"],
                    role=role,
                )
                session.add(user)

            for task in fixtures["tasks"]:
                responsible = session.get(User, task["responsible"])
                performers = get_users_by_id(session, task["performers"])
                task = Task(
                    title=task["title"],
                    description=task["description"],
                    priority=task["priority"],
                    responsible=responsible,
                    performers=performers,
                )
                session.add(task)

            session.commit()
