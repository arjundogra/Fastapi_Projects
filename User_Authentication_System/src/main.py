from fastapi import FastAPI
from routes.users import userRouter
from database_connection import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(userRouter,prefix='/users')