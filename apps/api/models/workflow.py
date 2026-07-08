from pydantic import BaseModel


class StepSummary(BaseModel):
    id: str
    name: str
    type: str  # "serviceTask" | "userTask" | "intermediateCatchEvent"
    documentation_path: str | None = None


class PhaseSummary(BaseModel):
    id: str
    name: str
    steps: list[StepSummary]


class WorkflowSummary(BaseModel):
    id: str
    name: str
    version: int
    definition_key: str


class WorkflowDetail(BaseModel):
    id: str
    name: str
    version: int
    definition_key: str
    phases: list[PhaseSummary]


class StepDocumentation(BaseModel):
    step_name: str
    content: str
