import httpx

TASKLIST_URL = "http://localhost:8082"
TASKLIST_AUTH = ("demo", "demo")


async def list_tasks(instance_id: str) -> list[dict[str, str | None]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TASKLIST_URL}/v1/tasks/search",
            auth=TASKLIST_AUTH,
            json={"processInstanceKey": instance_id, "state": "CREATED", "pageSize": 50},
        )
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]


async def complete_task(task_id: str, variables: dict[str, str]) -> None:
    async with httpx.AsyncClient() as client:
        # Tasklist requires the task to be assigned before it can be completed.
        await client.patch(
            f"{TASKLIST_URL}/v1/tasks/{task_id}/assign",
            auth=TASKLIST_AUTH,
            json={"assignee": "demo", "allowOverrideAssignment": True},
        )
        response = await client.patch(
            f"{TASKLIST_URL}/v1/tasks/{task_id}/complete",
            auth=TASKLIST_AUTH,
            json={"variables": [{"name": k, "value": v} for k, v in variables.items()]},
        )
        response.raise_for_status()
