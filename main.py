from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

app = FastAPI()
tasks = []

class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

@app.get("/")
def read_root():
    return {"message": "API is running..."}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Create a task
@app.post("/tasks")
def create_task(title: str):
    task = {
        "id": str(uuid4()),
        "title": title,
        "completed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    tasks.append(task)
    return task

# Delete a task by its ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# Update a task by its ID
@app.patch("/tasks/{task_id}")
def update_task(task_id: str, title: str):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["updated_at"] = datetime.now()
            return {"message": f"Task {task_id} updated successfully"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: str):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            task["updated_at"] = datetime.now()
            return {"message": f"Task {task_id} completed successfully"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)