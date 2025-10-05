from fastapi import APIRouter

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.get("/tasks")
async def read_tasks():
    return [{"task_id": 1, "title": "Task One"}, {"task_id": 2, "title": "Task Two"}]