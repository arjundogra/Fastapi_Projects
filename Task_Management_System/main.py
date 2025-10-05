from fastapi import FastAPI
from routes import users, tasks
from database_connection import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)