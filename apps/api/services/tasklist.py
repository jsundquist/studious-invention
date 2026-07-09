import httpx

TASKLIST_URL = "http://localhost:8082"
TASKLIST_AUTH = ("demo", "demo")


async def complete_task(task_id: str, variables: dict[str, str]) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{TASKLIST_URL}/v1/tasks/{task_id}/complete",
            auth=TASKLIST_AUTH,
            json={"variables": [{"name": k, "value": v} for k, v in variables.items()]},
        )
        response.raise_for_status()
