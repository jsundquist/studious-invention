import os

from fastapi import FastAPI

from logging_config import configure_logging
from routers.instances import router as instances_router
from routers.workflows import router as workflows_router

configure_logging(log_level=os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(
    title="Studious Invention API",
    description="Internal Developer Platform — golden path workflow management",
    version="0.1.0",
)

app.include_router(workflows_router)
app.include_router(instances_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
