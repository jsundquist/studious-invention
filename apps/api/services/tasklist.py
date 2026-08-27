import httpx

from config import config


def _auth() -> tuple[str, str]:
    return (config.tasklist_user, config.tasklist_password)


async def list_tasks(instance_id: str) -> list[dict[str, str | None]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.tasklist_url}/v1/tasks/search",
            auth=_auth(),
            json={"processInstanceKey": instance_id, "state": "CREATED", "pageSize": 50},
        )
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]


async def complete_task(task_id: str, variables: dict[str, str]) -> None:
    async with httpx.AsyncClient() as client:
        # Tasklist requires the task to be assigned before it can be completed.
        await client.patch(
            f"{config.tasklist_url}/v1/tasks/{task_id}/assign",
            auth=_auth(),
            json={"assignee": config.tasklist_user, "allowOverrideAssignment": True},
        )
        response = await client.patch(
            f"{config.tasklist_url}/v1/tasks/{task_id}/complete",
            auth=_auth(),
            json={"variables": [{"name": k, "value": v} for k, v in variables.items()]},
        )
        response.raise_for_status()
