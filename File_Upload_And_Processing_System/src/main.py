from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import users, files
from database_connection import engine, Base

app = FastAPI(title="File Upload And Processing System", version="1.0")
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(files.router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
        <head>
            <title>FastAPI</title>
        </head>
        <body>
            <h1>File Upload And Processing System!</h1>
            <p>Open <a href="/docs">API Documentation</a> for more details.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)