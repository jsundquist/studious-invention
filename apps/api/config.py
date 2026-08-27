from pydantic_settings import BaseSettings


class Config(BaseSettings):
    operate_url: str = "http://localhost:8081"
    operate_user: str = "demo"
    operate_password: str = "demo"
    tasklist_url: str = "http://localhost:8082"
    tasklist_user: str = "demo"
    tasklist_password: str = "demo"
    zeebe_address: str = "localhost:26500"
    log_level: str = "INFO"


config = Config()
