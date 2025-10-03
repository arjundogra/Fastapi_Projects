from fastapi import FastAPI
from database_connection import Base,engine
from models.books import Books
from routes.books import bookRouter

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(bookRouter,prefix='/books')

# @app.get("/")
# def abc():
#     return {'abc':"ABC"}