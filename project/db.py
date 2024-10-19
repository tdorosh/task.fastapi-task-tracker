from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlmodel import Session, create_engine, select

from project.db_models import Role, User
from project.utilities import get_password_hash

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_user(**kwargs) -> User:
    password = kwargs.pop("password")
    kwargs.update({"password": get_password_hash(password)})
    user = User(**kwargs)
    return user


def get_users_by_id(session, user_ids: Sequence[int]) -> list[User]:
    return list(session.exec(select(User).where(User.id.in_(user_ids))))


def get_user_by_name(username: str) -> User | None:
    with Session(engine) as session:
        statement = (
            select(User).options(joinedload(User.role)).where(User.name == username)
        )
        return session.exec(statement).first()


def get_all_roles() -> Sequence[Role]:
    with Session(engine) as session:
        return session.exec(select(Role)).all()
