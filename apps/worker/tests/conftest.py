from collections.abc import Callable
from typing import Any

import pytest


class FakeZeebeWorker:
    """Captures @worker.task-decorated functions instead of talking to Zeebe."""

    def __init__(self) -> None:
        self.tasks: dict[str, Callable[..., Any]] = {}

    def task(self, task_type: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self.tasks[task_type] = fn
            return fn

        return decorator


@pytest.fixture
def fake_worker() -> FakeZeebeWorker:
    return FakeZeebeWorker()
