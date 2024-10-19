from argparse import ArgumentParser
from getpass import getpass

from sqlmodel import Session

from project.db import create_db_user, engine

parser = ArgumentParser()

parser.add_argument("--func", "-f")

args = parser.parse_args()


def add_user():
    try:
        with Session(engine) as session:
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = getpass("Enter password: ")
            user = create_db_user(name=username, email=email, password=password)
            session.add(user)
            session.commit()
            print("User was added successfully.")
    except Exception as error:
        print(f"Error during adding user: {error}")


if args.func is not None:
    match args.func:
        case "add_user":
            add_user()
        case _:
            print("Function not recognized")
