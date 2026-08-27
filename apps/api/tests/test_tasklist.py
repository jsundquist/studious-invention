import httpx
import pytest
import respx

import services.tasklist as tasklist


@respx.mock
async def test_list_tasks_returns_json_body() -> None:
    respx.post(f"{tasklist.TASKLIST_URL}/v1/tasks/search").mock(
        return_value=httpx.Response(200, json=[{"id": "task-1", "name": "Review"}])
    )

    result = await tasklist.list_tasks("instance-1")

    assert result == [{"id": "task-1", "name": "Review"}]


@respx.mock
async def test_complete_task_assigns_before_completing() -> None:
    assign_route = respx.patch(f"{tasklist.TASKLIST_URL}/v1/tasks/task-1/assign").mock(
        return_value=httpx.Response(200)
    )
    complete_route = respx.patch(f"{tasklist.TASKLIST_URL}/v1/tasks/task-1/complete").mock(
        return_value=httpx.Response(200)
    )

    await tasklist.complete_task("task-1", {"outcome": "approved"})

    assert assign_route.called
    assert complete_route.called


@respx.mock
async def test_complete_task_raises_on_upstream_failure() -> None:
    respx.patch(f"{tasklist.TASKLIST_URL}/v1/tasks/task-1/assign").mock(
        return_value=httpx.Response(200)
    )
    respx.patch(f"{tasklist.TASKLIST_URL}/v1/tasks/task-1/complete").mock(
        return_value=httpx.Response(500)
    )

    with pytest.raises(httpx.HTTPStatusError):
        await tasklist.complete_task("task-1", {"outcome": "approved"})
