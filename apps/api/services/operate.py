import xml.etree.ElementTree as ET
from contextlib import asynccontextmanager

import httpx

from models.workflow import PhaseSummary, StepSummary, WorkflowDetail, WorkflowSummary

OPERATE_URL = "http://localhost:8081"
OPERATE_USER = "demo"
OPERATE_PASSWORD = "demo"

BPMN_NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}


@asynccontextmanager
async def _session():
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{OPERATE_URL}/api/login",
            data={"username": OPERATE_USER, "password": OPERATE_PASSWORD},
        )
        yield client


async def list_process_definitions() -> list[WorkflowSummary]:
    async with _session() as client:
        response = await client.post(
            f"{OPERATE_URL}/v1/process-definitions/search",
            json={"filter": {}, "size": 100},
        )
        response.raise_for_status()
        data = response.json()
        return [
            WorkflowSummary(
                id=d["bpmnProcessId"],
                name=d.get("name") or d["bpmnProcessId"],
                version=d["version"],
                definition_key=str(d["key"]),
            )
            for d in data.get("items", [])
        ]


async def get_process_definition(name: str) -> WorkflowDetail | None:
    async with _session() as client:
        search = await client.post(
            f"{OPERATE_URL}/v1/process-definitions/search",
            json={"filter": {"bpmnProcessId": name}, "size": 1},
        )
        search.raise_for_status()
        items = search.json().get("items", [])
        if not items:
            return None

        definition = items[0]
        key = definition["key"]

        xml_response = await client.get(f"{OPERATE_URL}/v1/process-definitions/{key}/xml")
        xml_response.raise_for_status()
        bpmn_xml = xml_response.text

    phases = _parse_phases_from_bpmn(bpmn_xml)
    return WorkflowDetail(
        id=definition["bpmnProcessId"],
        name=definition.get("name") or definition["bpmnProcessId"],
        version=definition["version"],
        definition_key=str(key),
        phases=phases,
    )


def _parse_phases_from_bpmn(bpmn_xml: str) -> list[PhaseSummary]:
    root = ET.fromstring(bpmn_xml)
    process = root.find("bpmn:process", BPMN_NS)
    if process is None:
        return []

    phases = []
    for sub in process.findall("bpmn:subProcess", BPMN_NS):
        steps = []
        for tag, task_type in [
            ("bpmn:serviceTask", "serviceTask"),
            ("bpmn:userTask", "userTask"),
            ("bpmn:intermediateCatchEvent", "intermediateCatchEvent"),
        ]:
            for task in sub.findall(tag, BPMN_NS):
                doc_el = task.find("bpmn:documentation", BPMN_NS)
                steps.append(
                    StepSummary(
                        id=task.get("id", ""),
                        name=task.get("name") or task.get("id") or "",
                        type=task_type,
                        documentation_path=doc_el.text if doc_el is not None else None,
                    )
                )
        phases.append(
            PhaseSummary(
                id=sub.get("id", ""),
                name=sub.get("name") or sub.get("id") or "",
                steps=steps,
            )
        )
    return phases


async def get_instance(instance_id: str) -> dict | None:
    async with _session() as client:
        response = await client.get(f"{OPERATE_URL}/v1/process-instances/{instance_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


async def get_active_elements(instance_id: str) -> list[dict]:
    async with _session() as client:
        response = await client.post(
            f"{OPERATE_URL}/v1/flow-node-instances/search",
            json={
                "filter": {"processInstanceKey": int(instance_id), "state": "ACTIVE"},
                "size": 50,
            },
        )
        response.raise_for_status()
        return response.json().get("items", [])


async def get_completed_elements(instance_id: str) -> list[dict]:
    async with _session() as client:
        response = await client.post(
            f"{OPERATE_URL}/v1/flow-node-instances/search",
            json={
                "filter": {"processInstanceKey": int(instance_id), "state": "COMPLETED"},
                "size": 200,
            },
        )
        response.raise_for_status()
        return response.json().get("items", [])
