from collections.abc import Awaitable, Callable
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest
from github import GithubException
from pyzeebe import ZeebeWorker
from pyzeebe.errors import BusinessError

from config import config
from handlers import provisioning
from tests.conftest import FakeZeebeWorker


@pytest.fixture(autouse=True)
def _reset_config() -> None:
    config.github_token = "fake-token"
    config.github_admin_team = ""
    config.github_repo_visibility = "private"


def _registered_handler(
    fake_worker: FakeZeebeWorker,
) -> Callable[..., Awaitable[dict[str, Any]]]:
    provisioning.register(cast(ZeebeWorker, fake_worker))
    return fake_worker.tasks["scaffold-repository"]


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_raises_business_error_when_org_missing(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    mock_gh = mock_github_cls.return_value
    mock_gh.get_organization.side_effect = GithubException(404, {"message": "Not Found"}, {})

    handler = _registered_handler(fake_worker)

    with pytest.raises(BusinessError, match="ORG_NOT_FOUND"):
        await handler(repo_name="my-service", repo_org="my-org")


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_reraises_non_404_org_errors(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    mock_gh = mock_github_cls.return_value
    mock_gh.get_organization.side_effect = GithubException(500, {"message": "boom"}, {})

    handler = _registered_handler(fake_worker)

    with pytest.raises(GithubException):
        await handler(repo_name="my-service", repo_org="my-org")


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_raises_business_error_when_repo_exists(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    mock_gh = mock_github_cls.return_value
    mock_org = mock_gh.get_organization.return_value
    mock_org.get_repo.return_value = MagicMock()  # repo already exists, no exception raised

    handler = _registered_handler(fake_worker)

    with pytest.raises(BusinessError, match="REPO_ALREADY_EXISTS"):
        await handler(repo_name="my-service", repo_org="my-org")


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_creates_repo_and_sets_branch_protection(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    mock_gh = mock_github_cls.return_value
    mock_org = mock_gh.get_organization.return_value
    mock_org.get_repo.side_effect = GithubException(404, {"message": "Not Found"}, {})

    mock_repo = MagicMock(clone_url="https://github.com/my-org/my-service.git")
    mock_org.create_repo.return_value = mock_repo

    handler = _registered_handler(fake_worker)

    result = await handler(repo_name="my-service", repo_org="my-org")

    mock_org.create_repo.assert_called_once()
    assert mock_org.create_repo.call_args.kwargs["private"] is True
    mock_repo.get_branch.assert_called_once_with("main")
    mock_repo.get_branch.return_value.edit_protection.assert_called_once()
    assert result == {"repo_url": "https://github.com/my-org/my-service.git"}


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_grants_admin_team_when_configured(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    config.github_admin_team = "platform-admins"
    mock_gh = mock_github_cls.return_value
    mock_org = mock_gh.get_organization.return_value
    mock_org.get_repo.side_effect = GithubException(404, {"message": "Not Found"}, {})
    mock_repo = MagicMock(clone_url="https://github.com/my-org/my-service.git")
    mock_org.create_repo.return_value = mock_repo

    handler = _registered_handler(fake_worker)

    await handler(repo_name="my-service", repo_org="my-org")

    mock_org.get_team_by_slug.assert_called_once_with("platform-admins")
    mock_org.get_team_by_slug.return_value.update_team_repository.assert_called_once_with(
        mock_repo, "admin"
    )


@patch("handlers.provisioning.Github")
async def test_scaffold_repository_public_visibility(
    mock_github_cls: MagicMock, fake_worker: FakeZeebeWorker
) -> None:
    config.github_repo_visibility = "public"
    mock_gh = mock_github_cls.return_value
    mock_org = mock_gh.get_organization.return_value
    mock_org.get_repo.side_effect = GithubException(404, {"message": "Not Found"}, {})
    mock_org.create_repo.return_value = MagicMock(clone_url="https://x")

    handler = _registered_handler(fake_worker)

    await handler(repo_name="my-service", repo_org="my-org")

    assert mock_org.create_repo.call_args.kwargs["private"] is False
