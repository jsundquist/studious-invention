from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

import routers.workflows as workflows_router
import services.operate as operate
from main import app
from models.workflow import PhaseSummary, StepSummary, WorkflowDetail, WorkflowSummary

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_docs_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(workflows_router, "DOCS_DIR", tmp_path / "docs" / "steps")


def test_list_workflows_returns_service_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        operate,
        "list_process_definitions",
        AsyncMock(
            return_value=[
                WorkflowSummary(id="wf-1", name="Workflow 1", version=1, definition_key="1")
            ]
        ),
    )

    response = client.get("/workflows")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "wf-1", "name": "Workflow 1", "version": 1, "definition_key": "1"}
    ]


def test_get_workflow_404_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=None))

    response = client.get("/workflows/missing")

    assert response.status_code == 404


def test_get_step_documentation_reads_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    detail = WorkflowDetail(
        id="wf-1",
        name="Workflow 1",
        version=1,
        definition_key="1",
        phases=[
            PhaseSummary(
                id="phase-1",
                name="Phase 1",
                steps=[
                    StepSummary(
                        id="review-task",
                        name="Review Task",
                        type="userTask",
                        documentation_path="docs/steps/review-task.md",
                    )
                ],
            )
        ],
    )
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=detail))

    # DOCS_DIR is monkeypatched to tmp_path/docs/steps; the router resolves the
    # doc path relative to DOCS_DIR.parent.parent, i.e. tmp_path itself.
    doc_file = tmp_path / "docs" / "steps" / "review-task.md"
    doc_file.parent.mkdir(parents=True)
    doc_file.write_text("# Review Task\n\nDo the review.")

    response = client.get("/workflows/wf-1/steps/review-task")

    assert response.status_code == 200
    body = response.json()
    assert body["step_name"] == "review-task"
    assert "Do the review." in body["content"]


def test_get_step_documentation_404_when_step_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    detail = WorkflowDetail(id="wf-1", name="Workflow 1", version=1, definition_key="1", phases=[])
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=detail))

    response = client.get("/workflows/wf-1/steps/nonexistent")

    assert response.status_code == 404


def test_get_step_documentation_404_when_file_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    detail = WorkflowDetail(
        id="wf-1",
        name="Workflow 1",
        version=1,
        definition_key="1",
        phases=[
            PhaseSummary(
                id="phase-1",
                name="Phase 1",
                steps=[
                    StepSummary(
                        id="review-task",
                        name="Review Task",
                        type="userTask",
                        documentation_path="docs/steps/does-not-exist.md",
                    )
                ],
            )
        ],
    )
    monkeypatch.setattr(operate, "get_process_definition", AsyncMock(return_value=detail))

    response = client.get("/workflows/wf-1/steps/review-task")

    assert response.status_code == 404
