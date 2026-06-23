# Local Development

## Prerequisites

- Docker with Docker Compose

## Starting the Stack

```bash
docker compose up
```

On first run, Docker will pull all images before starting. Subsequent starts are faster. The stack is ready when all services report healthy — Elasticsearch takes the longest to initialize.

## Services and Ports

| Service | URL | Purpose |
|---------|-----|---------|
| Zeebe | `localhost:26500` | Workflow engine (gRPC) |
| Zeebe REST API | `localhost:8080` | Workflow engine (REST) |
| Operate | `localhost:8081` | Workflow monitoring and execution history |
| Tasklist | `localhost:8082` | Human task management (operator/admin use) |
| Elasticsearch | `localhost:9200` | History storage (backing Operate) |

## Workflow Definitions

BPMN files in `workflows/` are automatically deployed to Zeebe on startup. Add or update a `.bpmn` file and restart the stack to redeploy.

## Stopping the Stack

```bash
# Stop but preserve data volumes
docker compose stop

# Full teardown including volumes (clean slate on next start)
docker compose down -v
```

Note: `docker compose down -v` removes all Elasticsearch data. Workflow definitions are redeployed automatically on next startup from the files in `workflows/`, but execution history is lost.

## Checking Health

```bash
# Overall stack status
docker compose ps

# Elasticsearch health
curl http://localhost:9200/_cat/health

# Zeebe health
curl http://localhost:8080/actuator/health
```
