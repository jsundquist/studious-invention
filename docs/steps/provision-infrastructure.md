# Provision Infrastructure

## What happens

Cloud infrastructure is provisioned for the service using the company's standard infrastructure template. Resources created include:

- Compute instance(s) sized to the selected tier
- Virtual network and firewall rules restricting inbound traffic to the API gateway only
- Load balancer with health check configuration pointing to `GET /health`
- Object storage bucket for application assets if required
- DNS record registered under the company's internal service domain

## What you need to provide

The following are collected when starting the workflow:

- **Infrastructure tier** — determines compute size and redundancy (e.g. small, medium, large)
- **Region** — where the service will be deployed
- **Requires persistent storage** — whether a managed database or file storage is needed (database provisioning is a separate workflow)

## What to expect

Infrastructure is provisioned in a staging environment first. Production infrastructure is not created until Phase 5. The staging environment is fully functional and is where the Deploy to Staging step will deploy your service.

Staging environment details (endpoint, credentials) are stored in secrets management and injected into the deployment automatically.
