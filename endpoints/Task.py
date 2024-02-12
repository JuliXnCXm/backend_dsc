from schemas.Task import Task , TaskStatus
from fastapi import APIRouter, status,HTTPException, Request, UploadFile, File
from connection import ConnDb
from controllers.TokenController import TokenController
from controllers.TaskController import get_all_tasks, create_task , get_tasks_lists_names, get_task, delete_task
from datetime import timedelta


router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    path="/tasks/alltask",
    tags=["Task"],
    summary="Task",
    description="get user tasks",
    response_description="All tasks information",
    status_code=status.HTTP_200_OK)
def retreieve_all_tasks(req: Request):
    try:
        db = next(ConnDb.Connection().get_db())
        user_id = TokenController(req).decodeToken()
        tasks = get_all_tasks(db,user_id)
        return {"tasks" : tasks}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    
@router.get(
    path="/tasks/categories",
    tags=["Task"],
    summary="Task",
    description="get user tasks categories",
    response_description="All tasks information",
    status_code=status.HTTP_200_OK)
def retreieve_categories(req: Request):
    try:
        db = next(ConnDb.Connection().get_db())
        user_id = TokenController(req).decodeToken()
        categories = get_tasks_lists_names(db,user_id)
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.put(
    path="/tasks/task",
    tags=["Task"],
    summary="Task",
    description="update user tasks",
    response_description="update task information",
    status_code=status.HTTP_201_CREATED)
def update_task(req: Request, task:dict):
    db = next(ConnDb.Connection().get_db())
    user_id = TokenController(req).decodeToken()
    db_task = get_task(db=db, user_id=user_id, task_id=task["id"])
    if task :
        for key, value in task.items():
            if key == "status":
                if value not in [TaskStatus.EMPEZADA.value, TaskStatus.FINALIZADA.value,TaskStatus.SIN_EMPEZAR.value]:
                    raise ValueError("Invalid status value")
                setattr(db_task, key, value)
            setattr(db_task, key, value)
    db.commit()
    return {"new_task": 
        {
                "id": db_task.id,
                "title": db_task.title,
                "description": db_task.description,
                "created_at": db_task.created_at,
                "completed_at": db_task.completed_at,
                "completed": db_task.completed,
                "status": db_task.status,
                "category": db_task.category
            } 
    }
    
    
@router.post(
    path="/tasks/task",
    tags=["Task"],
    summary="Task",
    description="create user tasks",
    response_description="create task information",
    status_code=status.HTTP_201_CREATED)
def create_task_per_user(req: Request, task: dict):
    try:
        db = next(ConnDb.Connection().get_db())
        user_id = TokenController(req).decodeToken()
        task = create_task(db,user_id,task)
        return task
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.delete(
    path="/tasks/{task_id}",
    tags=["Task"],
    summary="Task",
    description="delete user tasks",
    response_description="delete task",
    status_code=status.HTTP_200_OK)
def delete_task_per_user(req: Request, task_id: str):
    db = next(ConnDb.Connection().get_db())
    user_id = TokenController(req).decodeToken()
    db_task = delete_task(db=db, user_id=user_id, task_id=task_id)
    return {"message": "Task deleted successfully"}