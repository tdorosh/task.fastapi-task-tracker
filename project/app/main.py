from fastapi import FastAPI

from project.app.init import setup_initial_data
from project.app.routers import login, tasks

app = FastAPI()
app.include_router(login.router)
app.include_router(tasks.router)


@app.on_event("startup")
def on_startup():
    setup_initial_data()
