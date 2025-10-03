from fastapi import FastAPI
from database_connection import Base,engine
from routes.books import bookRouter
from routes.members import memberRouter

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(bookRouter,prefix='/books')
app.include_router(memberRouter,prefix='/members')

# @app.get("/")
# def abc():
#     return {'abc':"ABC"}