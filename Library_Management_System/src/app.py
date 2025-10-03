from fastapi import FastAPI
from database_connection import Base,engine
from routes.books import bookRouter
from routes.members import memberRouter
from routes.borrowRecords import borrowRecordRouter
from middleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

Base.metadata.create_all(engine)

app.include_router(bookRouter,prefix='/books')
app.include_router(memberRouter,prefix='/members')
app.include_router(borrowRecordRouter,prefix='/borrowRecords')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8080)
