import structlog
from github import Auth, Github, GithubException
from pyzeebe import ZeebeWorker
from pyzeebe.errors import BusinessError

from config import config

logger = structlog.get_logger(__name__)


def register(worker: ZeebeWorker) -> None:
    @worker.task(task_type="scaffold-repository")  # type: ignore[arg-type]
    async def scaffold_repository(
        repo_name: str, repo_org: str, **_kwargs: object
    ) -> dict[str, object]:
        log = logger.bind(repo_name=repo_name, repo_org=repo_org)
        gh = Github(auth=Auth.Token(config.github_token))

        try:
            org = gh.get_organization(repo_org)
        except GithubException as e:
            if e.status == 404:
                raise BusinessError(f"ORG_NOT_FOUND: {repo_org}") from e
            raise

        try:
            org.get_repo(repo_name)
            raise BusinessError(f"REPO_ALREADY_EXISTS: {repo_org}/{repo_name}")
        except GithubException as e:
            if e.status != 404:
                raise

        log.info("creating repository")
        is_private = config.github_repo_visibility != "public"
        repo = org.create_repo(
            name=repo_name,
            private=is_private,
            auto_init=True,  # pushes initial commit so 'main' branch exists for branch protection
            description=f"Service repository for {repo_name}",
        )

        repo.get_branch("main").edit_protection(
            required_approving_review_count=1,
            dismiss_stale_reviews=True,
        )

        if config.github_admin_team:
            org.get_team_by_slug(config.github_admin_team).update_team_repository(repo, "admin")

        log.info("repository created", repo_url=repo.clone_url)
        return {"repo_url": repo.clone_url}
