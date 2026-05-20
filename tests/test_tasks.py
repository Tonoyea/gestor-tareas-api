"""Tests para verificar que no se pueden modificar tareas finalizadas (status=done)."""

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from aplicacion.base_de_datos import Base, get_db
from aplicacion.principal import app

# Base de datos en memoria para tests
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def _create_task(title="Tarea de prueba", status="pending"):
    resp = client.post("/tasks/", json={"title": title, "status": status})
    assert resp.status_code == 201
    return resp.json()


# ── Tests para la condición de tarea finalizada ─────────────────────


def test_update_done_task_returns_400():
    """PATCH sobre una tarea con status=done debe devolver 400."""
    task = _create_task(status="done")
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Nuevo título"})
    assert resp.status_code == 400
    assert "finalizada" in resp.json()["detail"].lower()


def test_update_done_task_status_returns_400():
    """Intentar cambiar el status de una tarea done también debe devolver 400."""
    task = _create_task(status="done")
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "pending"})
    assert resp.status_code == 400


def test_update_pending_task_succeeds():
    """PATCH sobre una tarea pending debe funcionar normalmente."""
    task = _create_task(status="pending")
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Título actualizado"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Título actualizado"


def test_update_in_progress_task_succeeds():
    """PATCH sobre una tarea in_progress debe funcionar normalmente."""
    task = _create_task(status="in_progress")
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Nuevo"})
    assert resp.status_code == 200


def test_transition_to_done_allowed():
    """Cambiar una tarea pending a done debe estar permitido."""
    task = _create_task(status="pending")
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_done_task_not_modified_after_rejected_patch():
    """Verificar que la tarea done no se modifica tras un PATCH rechazado."""
    task = _create_task(title="Original", status="done")
    client.patch(f"/tasks/{task['id']}", json={"title": "Modificado"})
    resp = client.get(f"/tasks/{task['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Original"
