from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from datetime import datetime, UTC
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
@app.get("/get-tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return [Task.model_validate(task) for task in tasks]

# Create a task
@app.post("/create-task")
def create_task(title: str, description: str | None = None, db: Session = Depends(get_db)):
    task = TaskDB(title=title, description=description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return Task.model_validate(task)

# Delete a task by its ID
@app.delete("/delete-task/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}

# Update a task by its ID
@app.patch("/update-task/{task_id}")
def update_task(task_id: str, title: str, description: str | None = None, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    task.title = title
    if description:
        task.description = description
    task.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} updated successfully"}

@app.patch("/complete-task/{task_id}")
def complete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    task.completed = True
    task.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} completed successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)