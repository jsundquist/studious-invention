from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

import services.operate as operate
import services.tasklist as tasklist
import services.zeebe as zeebe
from main import app
from models.workflow import WorkflowDetail

client = TestClient(app)

SOME_DEFINITION = WorkflowDetail(
    id="wf-1", name="Workflow 1", version=1, definition_key="1", phases=[]
)


def test_start_instance_404_when_workflow_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=None))

    response = client.post("/instances", json={"workflow": "missing"})

    assert response.status_code == 404


def test_start_instance_returns_201_and_instance_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=SOME_DEFINITION))
    monkeypatch.setattr(zeebe, "start_process", AsyncMock(return_value="12345"))

    response = client.post("/instances", json={"workflow": "wf-1", "inputs": {"foo": "bar"}})

    assert response.status_code == 201
    assert response.json() == {"instance_id": "12345", "workflow": "wf-1", "state": "ACTIVE"}


def test_get_instance_404_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(operate, "get_instance", AsyncMock(return_value=None))

    response = client.get("/instances/999")

    assert response.status_code == 404


def test_get_instance_maps_active_elements(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "get_instance",
        AsyncMock(return_value={"bpmnProcessId": "wf-1", "state": "ACTIVE"}),
    )
    monkeypatch.setattr(
        operate,
        "get_active_elements",
        AsyncMock(
            return_value=[
                {
                    "flowNodeId": "review-task",
                    "flowNodeName": "Review Task",
                    "type": "userTask",
                    "startDate": "2026-08-27T00:00:00Z",
                }
            ]
        ),
    )

    response = client.get("/instances/1")

    assert response.status_code == 200
    body = response.json()
    assert body["workflow"] == "wf-1"
    assert body["active_elements"][0]["element_id"] == "review-task"


def test_list_tasks_maps_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "get_instance",
        AsyncMock(return_value={"bpmnProcessId": "wf-1", "state": "ACTIVE"}),
    )
    monkeypatch.setattr(
        tasklist,
        "list_tasks",
        AsyncMock(
            return_value=[
                {
                    "id": "task-1",
                    "taskDefinitionId": "review-task",
                    "name": "Review",
                    "assignee": None,
                }
            ]
        ),
    )

    response = client.get("/instances/1/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "task_id": "task-1",
            "element_id": "review-task",
            "element_name": "Review",
            "assignee": None,
        }
    ]


def test_complete_task_requires_reason_when_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "get_instance",
        AsyncMock(return_value={"bpmnProcessId": "wf-1", "state": "ACTIVE"}),
    )

    response = client.post(
        "/instances/1/tasks/task-1/complete", json={"outcome": "skipped", "reason": ""}
    )

    assert response.status_code == 422


def test_complete_task_502_on_upstream_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "get_instance",
        AsyncMock(return_value={"bpmnProcessId": "wf-1", "state": "ACTIVE"}),
    )
    monkeypatch.setattr(tasklist, "complete_task", AsyncMock(side_effect=RuntimeError("boom")))

    response = client.post("/instances/1/tasks/task-1/complete", json={"outcome": "approved"})

    assert response.status_code == 502


def test_complete_task_204_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "get_instance",
        AsyncMock(return_value={"bpmnProcessId": "wf-1", "state": "ACTIVE"}),
    )
    monkeypatch.setattr(tasklist, "complete_task", AsyncMock(return_value=None))

    response = client.post("/instances/1/tasks/task-1/complete", json={"outcome": "approved"})

    assert response.status_code == 204
