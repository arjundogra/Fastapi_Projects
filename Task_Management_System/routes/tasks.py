from fastapi import APIRouter
from models.users import Users
from models.tasks import Tasks
from sqlalchemy.orm import Session
from database_connection import get_db
from core.auth import verify_access_token
from fastapi import Depends, HTTPException, status
from schemas import tasks
from sqlalchemy import or_

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
    
@router.get("/fetch/{task_id}", response_model=tasks.TaskResponseModel)
def fetch_task(task_id: int, user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.created_by != user_id and task.assigned_to != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this task")
    return task

@router.get("/fetchAll", response_model=list[tasks.TaskResponseModel], status_code=status.HTTP_200_OK)
def fetch_all_tasks(user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_role = db.query(Users).filter(Users.id == user_id).first().role
    if user_role == 'admin':
        tasks = db.query(Tasks).all()
    else:
        tasks = db.query(Tasks).filter(or_(Tasks.created_by == user_id, Tasks.assigned_to == user_id)).all()
    return tasks

@router.patch("/update/{task_id}", response_model=tasks.TaskResponseModel,status_code=status.HTTP_200_OK)
def update_task(task_id: int,req: tasks.CreateTaskRequest, user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.created_by != user_id and task.assigned_to != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized")
    new_values = req.model_dump(exclude_unset=True)
    for key,value in new_values.items():
        if hasattr(task,key):
            setattr(task,key,value)
    db.commit()
    return  task

@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    if task.created_by != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Autherized for this action")
    db.delete(task)
    db.commit()
    return 