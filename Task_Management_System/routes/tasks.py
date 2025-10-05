from fastapi import APIRouter
from models.tasks import Tasks
from sqlalchemy.orm import Session
from database_connection import get_db
from core.auth import verify_access_token
from fastapi import Depends, HTTPException, status
from schemas import tasks

router = APIRouter(prefix="/tasks",tags=["Tasks"],dependencies=[Depends(verify_access_token)])

@router.post("/create", response_model=tasks.TaskResponseModel, status_code=status.HTTP_201_CREATED)
def create_task(req: tasks.CreateTaskRequest, user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    try:
        new_task = Tasks(title=req.title, description=req.description, status=req.status, created_by=user_id, due_date=req.due_date, assigned_to=req.assigned_to)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))