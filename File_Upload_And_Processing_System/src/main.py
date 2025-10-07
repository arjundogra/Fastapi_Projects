from fastapi import FastAPI
from routes import users, files

app = FastAPI(title="File Upload And Processing System", version="1.0")

app.include_router(users.router)
app.include_router(files.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)