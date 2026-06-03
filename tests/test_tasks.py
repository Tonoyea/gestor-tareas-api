# Tests de integración para los endpoints REST de tareas

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from aplicacion.base_de_datos import Base, get_db
from aplicacion.principal import app

# Base de datos SQLite en memoria para aislamiento entre tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    """Recrea las tablas antes de cada test y las elimina al terminar."""
    Base.metadata.create_all(bind=engine_test)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine_test)


# ── GET /tasks/ ──────────────────────────────────────────────────────────────

def test_list_tasks_empty(client):
    """Devuelve lista vacía cuando no hay tareas."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data(client):
    """Devuelve las tareas existentes."""
    client.post("/tasks/", json={"title": "Tarea 1"})
    client.post("/tasks/", json={"title": "Tarea 2"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Tarea 1"
    assert data[1]["title"] == "Tarea 2"


# ── POST /tasks/ ─────────────────────────────────────────────────────────────

def test_create_task_minimal(client):
    """Crea una tarea con solo el titulo (campos minimos)."""
    response = client.post("/tasks/", json={"title": "Nueva tarea"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nueva tarea"
    assert data["description"] is None
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


def test_create_task_full(client):
    """Crea una tarea con todos los campos proporcionados."""
    payload = {
        "title": "Tarea completa",
        "description": "Con descripcion",
        "status": "in_progress",
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarea completa"
    assert data["description"] == "Con descripcion"
    assert data["status"] == "in_progress"


def test_create_task_invalid_status(client):
    """Devuelve 422 si el estado no es valido."""
    response = client.post("/tasks/", json={"title": "Tarea", "status": "invalido"})
    assert response.status_code == 422


def test_create_task_missing_title(client):
    """Devuelve 422 si no se envia el titulo."""
    response = client.post("/tasks/", json={"description": "Sin titulo"})
    assert response.status_code == 422


# ── GET /tasks/{id} ──────────────────────────────────────────────────────────

def test_get_task_success(client):
    """Devuelve la tarea cuando existe."""
    create = client.post("/tasks/", json={"title": "Buscar esta"})
    task_id = create.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Buscar esta"


def test_get_task_not_found(client):
    """Devuelve 404 y detail cuando la tarea no existe."""
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ── PATCH /tasks/{id} ────────────────────────────────────────────────────────

def test_update_task_partial(client):
    """Actualiza solo el titulo sin modificar los demas campos."""
    create = client.post(
        "/tasks/",
        json={"title": "Original", "description": "Desc original"},
    )
    task_id = create.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": "Modificada"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Modificada"
    assert data["description"] == "Desc original"


def test_update_task_status(client):
    """Cambia el estado de una tarea."""
    create = client.post("/tasks/", json={"title": "Cambiar estado"})
    task_id = create.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_not_found(client):
    """Devuelve 404 y detail al intentar actualizar una tarea inexistente."""
    response = client.patch("/tasks/9999", json={"title": "No existe"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ── DELETE /tasks/{id} ───────────────────────────────────────────────────────

def test_delete_task_success(client):
    """Elimina una tarea y devuelve 204 sin cuerpo."""
    create = client.post("/tasks/", json={"title": "A eliminar"})
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Devuelve 404 y detail al intentar eliminar una tarea inexistente."""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
