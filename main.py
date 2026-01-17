from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from datetime import datetime
from sqlalchemy.orm import Session
from models import Task, TaskDB
from database import get_db, engine, Base

app = FastAPI()

# Create tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API is running..."}

# Get all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return [Task.model_validate(task) for task in tasks]

# Create a task
@app.post("/tasks")
def create_task(title: str, db: Session = Depends(get_db)):
    task_db = TaskDB(
        title=title,
        completed=False
    )
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return Task.model_validate(task_db)

# Delete a task by its ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}

# Update a task by its ID
@app.patch("/tasks/{task_id}")
def update_task(task_id: str, title: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    task.title = title
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} updated successfully"}

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    task.completed = True
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} completed successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)