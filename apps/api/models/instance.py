from typing import Any, Literal, Self

from pydantic import BaseModel, model_validator


class StartInstanceRequest(BaseModel):
    workflow: str
    inputs: dict[str, Any] = {}


class StartInstanceResponse(BaseModel):
    instance_id: str
    workflow: str
    state: str


class ActiveElement(BaseModel):
    element_id: str
    element_name: str | None
    element_type: str
    started_at: str | None


class InstanceStatus(BaseModel):
    instance_id: str
    workflow: str
    state: str
    active_elements: list[ActiveElement]


class HistoryEntry(BaseModel):
    element_id: str
    element_name: str | None
    element_type: str
    state: str
    started_at: str | None
    ended_at: str | None


class TaskCompleteRequest(BaseModel):
    outcome: Literal["approved", "skipped"]
    reason: str = ""

    @model_validator(mode="after")
    def require_reason_when_skipped(self) -> Self:
        if self.outcome == "skipped" and not self.reason:
            raise ValueError("reason is required when outcome is skipped")
        return self
