from starlette.middleware.base import BaseHTTPMiddleware
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        startTime = time.time()
        response = await call_next(request)
        processTime = time.time() - startTime
        print(f"Method: {request.method} || Time Taken: {processTime:.4f}")
        return response