"""Tests para el endpoint GET /tasks/status/{status}."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from aplicacion.base_de_datos import Base, get_db
from aplicacion.modelos import TaskStatus
from aplicacion.principal import app

# Base de datos en memoria para los tests
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _create_task(client: TestClient, title: str, status: str = "pending"):
    return client.post("/tasks/", json={"title": title, "status": status})


class TestListTasksByStatus:
    def test_returns_empty_list_when_no_tasks(self, client):
        resp = client.get("/tasks/status/pending")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_filters_by_pending(self, client):
        _create_task(client, "t1", "pending")
        _create_task(client, "t2", "done")

        resp = client.get("/tasks/status/pending")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "t1"
        assert data[0]["status"] == "pending"

    def test_filters_by_in_progress(self, client):
        _create_task(client, "t1", "in_progress")
        _create_task(client, "t2", "pending")

        resp = client.get("/tasks/status/in_progress")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["status"] == "in_progress"

    def test_filters_by_done(self, client):
        _create_task(client, "t1", "done")
        _create_task(client, "t2", "done")
        _create_task(client, "t3", "pending")

        resp = client.get("/tasks/status/done")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all(t["status"] == "done" for t in data)

    def test_invalid_status_returns_422(self, client):
        resp = client.get("/tasks/status/invalid")
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert detail[0]["loc"] == ["path", "status"]
        assert "pending" in detail[0]["msg"]
