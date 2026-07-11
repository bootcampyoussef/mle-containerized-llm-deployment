# Render Deployment

The checked-in `render.yaml` defines a Docker web service, a health-check path,
one starter instance, and secrets that must be entered in Render rather than
committed. It deploys the API container while Groq performs inference through an
OpenAI-compatible endpoint.

## Practice

Create a Render Blueprint from your repository and verify:

1. `/health` returns `200` after deployment;
2. `/ready` names the configured provider and model;
3. a valid `/generate` request succeeds; and
4. an empty prompt returns `422` without reaching the provider.

Record the deployed URL and the observed cold-start latency. Do not add the API
key to `render.yaml` or the repository.

## Reference Answer

`GROQ_API_KEY` uses `sync: false`, which makes Render request the value during
Blueprint creation. `healthCheckPath: /health` lets Render remove an unhealthy
instance from service without spending tokens on a readiness probe.
