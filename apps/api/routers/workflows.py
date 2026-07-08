from pathlib import Path

from fastapi import APIRouter, HTTPException

import services.operate as operate
from models.workflow import StepDocumentation, WorkflowDetail, WorkflowSummary

router = APIRouter(prefix="/workflows", tags=["workflows"])

DOCS_DIR = Path(__file__).parent.parent.parent.parent / "docs" / "steps"


@router.get("", response_model=list[WorkflowSummary])
async def list_workflows():
    return await operate.list_process_definitions()


@router.get("/{name}", response_model=WorkflowDetail)
async def get_workflow(name: str):
    detail = await operate.get_process_definition(name)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{name}' not found")
    return detail


def _find_doc_path(phases, step_name: str) -> str | None:
    for phase in phases:
        for step in phase.steps:
            if step.id == step_name or step.name.lower().replace(" ", "-") == step_name:
                return step.documentation_path
    return None


@router.get("/{name}/steps/{step_name}", response_model=StepDocumentation)
async def get_step_documentation(name: str, step_name: str):
    detail = await operate.get_process_definition(name)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{name}' not found")

    doc_path = _find_doc_path(detail.phases, step_name)

    if doc_path is None:
        raise HTTPException(
            status_code=404, detail=f"Step '{step_name}' not found in workflow '{name}'"
        )

    full_path = DOCS_DIR.parent.parent / doc_path
    if not full_path.exists():
        raise HTTPException(
            status_code=404, detail=f"Documentation file not found for step '{step_name}'"
        )

    return StepDocumentation(step_name=step_name, content=full_path.read_text())
