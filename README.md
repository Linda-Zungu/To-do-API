# Todo API

A simple RESTful API for managing todo tasks built with FastAPI and Python.

## Features

- Create new tasks
- Get all tasks
- Update task titles
- Mark tasks as completed
- Delete tasks
- Automatic task ID generation using UUID
- Timestamp tracking (created_at and updated_at)

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server by running:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

You can also access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Get API Status
- **GET** `/`
- Returns a simple status message

### Get All Tasks
- **GET** `/tasks`
- Returns a list of all tasks

**Response:**
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "completed": false,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
]
```

### Create a Task
- **POST** `/tasks?title=Your Task Title`
- Creates a new task with the provided title

**Parameters:**
- `title` (query parameter): The task title

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Your Task Title",
  "completed": false,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### Update a Task
- **PATCH** `/tasks/{task_id}?title=Updated Title`
- Updates the title of an existing task

**Parameters:**
- `task_id` (path parameter): The UUID of the task to update
- `title` (query parameter): The new task title

**Response:**
```json
{
  "message": "Task {task_id} updated successfully"
}
```

### Complete a Task
- **PATCH** `/tasks/{task_id}/complete`
- Marks a task as completed

**Parameters:**
- `task_id` (path parameter): The UUID of the task to complete

**Response:**
```json
{
  "message": "Task {task_id} completed successfully"
}
```

### Delete a Task
- **DELETE** `/tasks/{task_id}`
- Deletes a task by its ID

**Parameters:**
- `task_id` (path parameter): The UUID of the task to delete

**Response:**
```json
{
  "message": "Task {task_id} deleted successfully"
}
```

**Error Response (404):**
```json
{
  "detail": "Task {task_id} not found"
}
```

## Example Usage

### Using cURL

**Create a task:**
```bash
curl -X POST "http://localhost:8000/tasks?title=Buy groceries"
```

**Get all tasks:**
```bash
curl -X GET "http://localhost:8000/tasks"
```

**Update a task:**
```bash
curl -X PATCH "http://localhost:8000/tasks/{task_id}?title=Buy groceries and cook dinner"
```

**Complete a task:**
```bash
curl -X PATCH "http://localhost:8000/tasks/{task_id}/complete"
```

**Delete a task:**
```bash
curl -X DELETE "http://localhost:8000/tasks/{task_id}"
```

## Notes

- Tasks are stored in memory and will be lost when the server is restarted
- Each task is automatically assigned a unique UUID
- Tasks include automatic timestamp tracking for creation and updates

## Tests

Run the test suite with:

```bash
pytest
```

The tests use an in-memory SQLite database and do not require a running
Postgres instance.
