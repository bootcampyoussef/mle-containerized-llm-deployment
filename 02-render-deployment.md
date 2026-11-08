# Render Deployment

Translate the local container contract into a hosted one. You can complete
the configuration walkthrough without creating a Render service.

## Read The Blueprint

Open [render.yaml](render.yaml) alongside the [Dockerfile](Dockerfile).
The [Blueprint](https://render.com/docs/blueprint-spec) describes how Render
should build and run the service from Git. The container still runs FastAPI;
in live mode the external provider runs the model.

| Field | Follow it through the deployment |
|---|---|
| `runtime: docker`, `dockerfilePath`, `dockerContext` | Render builds the same Dockerfile from the repository root. It does not use the image already on your laptop. |
| `healthCheckPath: /health` | Render probes the lightweight HTTP route before routing traffic to the new instance. A passing check does not validate inference. |
| `plan: starter`, `numInstances: 1` | Instance size and replica count are separate choices. Start with one instance and gather evidence before scaling. |
| `envVars` | Runtime settings identify the provider. `sync: false` leaves the API key value outside Git. |

Read [Render's health-check behavior](https://render.com/docs/health-checks)
and predict what happens if the configured path is misspelled: the process can
start successfully while the deployment fails its HTTP check. Build logs,
startup logs, and health-check results answer different questions.

The Starter plan is paid. This teaching API has no authentication or per-client
rate limit: add access controls before exposing paid generation publicly, and
remove the service after the exercise to stop instance charges.

## Optional Hosted Walkthrough

Only create resources if your instructor has approved the account, cost, and
access setup. Otherwise, use the Blueprint table and the results from step 01
to explain how you would verify a hosted deployment.

1. In Render, create a Blueprint from the intended repository and branch.
   Check that the preview shows the intended Docker service and instance count
   before applying it.
2. Provide credentials through the dashboard, never the Dockerfile or Git.
   For a stub-only demo, set `MODEL_PROVIDER=dry` in your demo Blueprint and
   omit the API key entry. A hosted stub can still incur instance charges.
3. Once the deployment is live, repeat the requests from
   [step 01](01-container-contract.md#verify-the-api) using the hosted HTTPS URL.
   Expect 200 on health, readiness, and a valid generation, and 422 for a
   blank prompt. Check the response model to distinguish dry and live runs.

## Practice

For each verification request, note what an unexpected result would make you
inspect next: the health path, runtime settings, the provider, or input
validation. If you ran a hosted demo, record the deployed revision and label
first-request timings separately from later requests. A slow first request
alone does not identify whether the app, provider, or network caused the wait.
Remove the demo service when finished and check the dashboard for other
resources it created.

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
