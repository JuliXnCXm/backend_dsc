from sqlalchemy.orm import Session
from models.User import Task as task_model
from fastapi import status,HTTPException
import uuid
from datetime import datetime
def get_task_by_tagname(db: Session, email: str):
    return db.query(task_model).filter(task_model.email == email).first()


def get_all_tasks(db: Session, user_id: str):
    try :
        tasks = db.query(task_model).filter(task_model.owner_id == user_id).order_by(task_model.created_at.desc()).all()
        all_tasks = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at,
                "completed_at": task.completed_at,
                "completed": task.completed,
                "status": task.status,
                "category": task.category
            } for task in tasks]
        return all_tasks
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
def create_task(db:Session, user_id:str, task_data:dict):
    try:
        task_data["id"] = uuid.uuid4().hex
        task_data["created_at"] = datetime.now()
        print(task_data)
        db_task = task_model(**task_data, owner_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def get_task(db: Session, task_id:str, user_id:str):
    try:
        task = db.query(task_model).filter(task_model.id == task_id, task_model.owner_id == user_id).first()
        return task
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

def delete_task(db:Session, task_id:str, user_id:str):
    try:
        task = db.query(task_model).filter(task_model.id == task_id, task_model.owner_id == user_id).first()
        db.delete(task)
        db.commit()
        return task
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

def get_tasks_lists_names(db: Session, user_id: str):
    try :
        tasks = db.query(task_model).filter(task_model.owner_id == user_id).order_by(task_model.created_at.desc()).all()
        category_names = [x.category for x in tasks]
        return category_names
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))