# Setup and Running Guide

This guide will help you set up the virtual environment and run the Todo API application.

## Prerequisites

- Python 3.7 or higher installed on your system
- Terminal/Command line access

## Step 1: Create Virtual Environment (First Time Only)

If you haven't created a virtual environment yet, run:

```bash
python3 -m venv .venv
```

Or on some systems:

```bash
python -m venv .venv
```

## Step 2: Activate Virtual Environment

### On macOS/Linux:
```bash
source .venv/bin/activate
```

### On Windows:
```bash
.venv\Scripts\activate
```

After activation, you should see `(.venv)` at the beginning of your terminal prompt.

## Step 3: Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

Start the FastAPI server with auto-reload enabled:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables automatic reloading when you make changes to the code.

## Accessing the Application

Once the server is running, you can access:

- **API Base URL**: http://127.0.0.1:8000
- **Interactive API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc

## Running Tests

With the virtual environment activated, run:

```bash
pytest
```

The tests run against an in-memory SQLite database.

## Quick Start (All Steps Combined)

If you're starting fresh:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

## Deactivating Virtual Environment

When you're done working, you can deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

- **Port already in use**: If port 8000 is already in use, you can specify a different port:
  ```bash
  uvicorn main:app --reload --port 8001
  ```

- **Module not found errors**: Make sure the virtual environment is activated and dependencies are installed.

- **Python version issues**: Ensure you're using Python 3.7 or higher. Check with:
  ```bash
  python3 --version
  ```
