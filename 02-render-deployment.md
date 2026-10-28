# Render Deployment

The checked-in `render.yaml` defines a Docker web service, a health-check path,
one starter instance, and secrets that must be entered in Render rather than
committed. It deploys the API container while Groq performs inference through an
OpenAI-compatible endpoint.

The Starter plan is paid. This teaching API has no authentication or per-client
rate limit: add access controls before exposing paid generation publicly, and
remove the service after the exercise to stop instance charges.

## Practice

Create a Render Blueprint from your repository and verify:

1. `/health` returns `200` after deployment;
2. `/ready` names the configured provider and model;
3. a valid `/generate` request succeeds; and
4. an empty prompt returns `422` without reaching the provider.

Record the deployed URL and the observed cold-start latency. Do not add the API
key to `render.yaml` or the repository.

## Reference Answer

<details>
<summary>Show Reference Answer</summary>

`GROQ_API_KEY` uses `sync: false`, which makes Render request the value during
Blueprint creation. `healthCheckPath: /health` lets Render remove an unhealthy
instance from service without spending tokens on a readiness probe.

</details>

## Check Your Understanding

1. Is a working local container proof of a successful Render deployment?
2. Does removing the API key stop instance charges?

<details>
<summary>Show Reference Answers</summary>

1. No. Verify the deployed routes and runtime configuration separately.
2. No. Delete the paid service after the exercise; instance billing is separate from provider usage.

</details>
