import structlog
from fastapi import APIRouter, HTTPException

import services.operate as operate
import services.tasklist as tasklist
import services.zeebe as zeebe
from models.instance import (
    ActiveElement,
    HistoryEntry,
    InstanceStatus,
    StartInstanceRequest,
    StartInstanceResponse,
    TaskCompleteRequest,
)

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/instances", tags=["instances"])


@router.post("", response_model=StartInstanceResponse, status_code=201)
async def start_instance(body: StartInstanceRequest) -> StartInstanceResponse:
    definition = await operate.get_process_definition(body.workflow)
    if definition is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{body.workflow}' not found")

    instance_id = await zeebe.start_process(body.workflow, body.inputs)
    return StartInstanceResponse(
        instance_id=instance_id,
        workflow=body.workflow,
        state="ACTIVE",
    )


@router.get("/{instance_id}", response_model=InstanceStatus)
async def get_instance(instance_id: str) -> InstanceStatus:
    instance = await operate.get_instance(instance_id)
    if instance is None:
        raise HTTPException(status_code=404, detail=f"Instance '{instance_id}' not found")

    active_elements = await operate.get_active_elements(instance_id)
    return InstanceStatus(
        instance_id=instance_id,
        workflow=instance.get("bpmnProcessId", ""),
        state=instance.get("state", ""),
        active_elements=[
            ActiveElement(
                element_id=el.get("flowNodeId", ""),
                element_name=el.get("flowNodeName"),
                element_type=el.get("type", ""),
                started_at=el.get("startDate"),
            )
            for el in active_elements
        ],
    )


@router.get("/{instance_id}/history", response_model=list[HistoryEntry])
async def get_instance_history(instance_id: str) -> list[HistoryEntry]:
    instance = await operate.get_instance(instance_id)
    if instance is None:
        raise HTTPException(status_code=404, detail=f"Instance '{instance_id}' not found")

    completed = await operate.get_completed_elements(instance_id)
    return [
        HistoryEntry(
            element_id=el.get("flowNodeId", ""),
            element_name=el.get("flowNodeName"),
            element_type=el.get("type", ""),
            state=el.get("state", ""),
            started_at=el.get("startDate"),
            ended_at=el.get("endDate"),
        )
        for el in completed
    ]


@router.post("/{instance_id}/tasks/{task_id}/complete", status_code=204)
async def complete_task(instance_id: str, task_id: str, body: TaskCompleteRequest) -> None:
    instance = await operate.get_instance(instance_id)
    if instance is None:
        raise HTTPException(status_code=404, detail=f"Instance '{instance_id}' not found")

    variables: dict[str, str] = {"outcome": body.outcome}
    if body.reason:
        variables["reason"] = body.reason

    try:
        await tasklist.complete_task(task_id, variables)
    except Exception as e:
        logger.error("Failed to complete task %s: %s", task_id, e)
        raise HTTPException(
            status_code=502, detail="Failed to complete task — upstream service unavailable"
        )
