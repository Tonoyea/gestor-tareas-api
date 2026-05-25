# Tests de la API de gestión de tareas con pytest y FastAPI TestClient

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from aplicacion.base_de_datos import Base, get_db
from aplicacion.principal import app

engine_test = create_engine(
    "sqlite:///:memory:",
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


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine_test)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)


# ---------------------------------------------------------------------------
# POST /tasks/ — crear tarea
# ---------------------------------------------------------------------------

def test_crear_tarea_correctamente(client):
    payload = {"title": "Tarea de prueba", "description": "Descripción de ejemplo"}
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarea de prueba"
    assert data["description"] == "Descripción de ejemplo"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


# ---------------------------------------------------------------------------
# GET /tasks/ — listar tareas
# ---------------------------------------------------------------------------

def test_listar_tareas_vacio(client):
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_listar_tareas_con_datos(client):
    client.post("/tasks/", json={"title": "Primera tarea"})
    client.post("/tasks/", json={"title": "Segunda tarea"})

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# GET /tasks/{task_id} — obtener tarea por id
# ---------------------------------------------------------------------------

def test_obtener_tarea_por_id(client):
    crear = client.post("/tasks/", json={"title": "Tarea X"})
    task_id = crear.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Tarea X"


def test_obtener_tarea_inexistente_devuelve_404(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ---------------------------------------------------------------------------
# PATCH /tasks/{task_id} — actualizar tarea
# ---------------------------------------------------------------------------

def test_actualizar_tarea_parcialmente(client):
    crear = client.post("/tasks/", json={"title": "Original", "description": "Desc"})
    task_id = crear.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "Modificada"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Modificada"
    assert data["description"] == "Desc"


def test_actualizar_tarea_inexistente_devuelve_404(client):
    response = client.patch("/tasks/9999", json={"title": "X"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ---------------------------------------------------------------------------
# DELETE /tasks/{task_id} — eliminar tarea
# ---------------------------------------------------------------------------

def test_eliminar_tarea(client):
    crear = client.post("/tasks/", json={"title": "A eliminar"})
    task_id = crear.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_eliminar_tarea_inexistente_devuelve_404(client):
    response = client.delete("/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
