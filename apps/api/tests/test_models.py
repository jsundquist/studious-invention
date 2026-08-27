import pytest
from pydantic import ValidationError

from models.instance import TaskCompleteRequest


def test_approved_outcome_does_not_require_reason() -> None:
    req = TaskCompleteRequest(outcome="approved")
    assert req.reason == ""


def test_skipped_outcome_requires_reason() -> None:
    with pytest.raises(ValidationError, match="reason is required"):
        TaskCompleteRequest(outcome="skipped")


def test_skipped_outcome_with_reason_is_valid() -> None:
    req = TaskCompleteRequest(outcome="skipped", reason="not applicable")
    assert req.reason == "not applicable"
