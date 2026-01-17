import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


TEST_DATABASE_URL = "sqlite://"


@pytest.fixture()
def client():
    # Set environment variable FIRST, before any imports
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL

    # Remove modules from cache to force reimport
    for module_name in ("database", "main", "models"):
        if module_name in sys.modules:
            del sys.modules[module_name]

    # Create test engine
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    # Import database (will use TEST_DATABASE_URL from env)
    import database
    
    # Override engine and session before main imports them
    database.engine = test_engine
    database.SessionLocal = testing_session_local

    # Now import main (will import engine from database, which is now test_engine)
    import main
    
    # Also override main's engine reference (in case it cached it)
    main.engine = test_engine

    # Create tables with test engine
    database.Base.metadata.drop_all(bind=test_engine)
    database.Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[main.get_db] = override_get_db

    with TestClient(main.app) as test_client:
        yield test_client

    main.app.dependency_overrides.clear()


def _create_task(client, title="Buy milk", description="Remember lactose free"):
    response = client.post(
        "/create-task",
        params={"title": title, "description": description},
    )
    assert response.status_code == 200
    return response.json()


def test_root_returns_status(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is running..."}


def test_create_task_and_list_tasks(client):
    created = _create_task(client)

    list_response = client.get("/get-tasks")

    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created["id"]
    assert tasks[0]["title"] == created["title"]


def test_update_task_changes_fields(client):
    created = _create_task(client)

    response = client.patch(
        f"/update-task/{created['id']}",
        params={"title": "Buy bread", "description": "Whole grain"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {created['id']} updated successfully"

    tasks = client.get("/get-tasks").json()
    assert tasks[0]["title"] == "Buy bread"
    assert tasks[0]["description"] == "Whole grain"


def test_complete_task_marks_completed(client):
    created = _create_task(client)

    response = client.patch(f"/complete-task/{created['id']}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {created['id']} completed successfully"

    tasks = client.get("/get-tasks").json()
    assert tasks[0]["completed"] is True


def test_delete_task_removes_record(client):
    created = _create_task(client)

    response = client.delete(f"/delete-task/{created['id']}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {created['id']} deleted successfully"
    assert client.get("/get-tasks").json() == []


def test_delete_missing_task_returns_404(client):
    response = client.delete("/delete-task/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task does-not-exist not found"
