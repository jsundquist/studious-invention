from pydantic_settings import BaseSettings


class Config(BaseSettings):
    zeebe_address: str = "localhost:26500"
    log_level: str = "INFO"
    github_token: str = ""
    github_admin_team: str = ""
    github_repo_visibility: str = "private"


config = Config()
