# Render Deployment

Deploy the container from [step 01](01-container-contract.md) on a single
[Free Render web service](https://render.com/docs/free). Groq is the default
and needs an API key. Use dry mode to verify the deployment without a key,
or stay local if you do not want to create a Render account.

## Read The Blueprint

Open [render.yaml](render.yaml) alongside the [Dockerfile](Dockerfile).
The [Blueprint](https://render.com/docs/blueprint-spec) describes how Render
should build and run the service from Git. The container still runs FastAPI;
in live mode the external provider runs the model.

| Field | Follow it through the deployment |
|---|---|
| `runtime: docker`, `dockerfilePath`, `dockerContext` | Render builds the same Dockerfile from the repository root. It does not use the image already on your laptop. |
| `PORT=8000`, `healthCheckPath: /health` | The port matches the Dockerfile. Render probes this route before routing traffic to the new instance; a passing check does not validate inference. |
| `plan: free` | Render runs one instance. It can sleep when idle; the first request after that may be slow. |
| `MODEL_PROVIDER=groq`, `GROQ_API_KEY` | Groq runs the model. `sync: false` prompts for the key in Render instead of storing it in Git. |

Read [Render's health-check behavior](https://render.com/docs/health-checks)
and predict what happens if the configured path is misspelled: the process can
start successfully while the deployment fails its HTTP check. Build logs,
startup logs, and health-check results answer different questions.

## Optional Hosted Walkthrough

To deploy without a key, set `MODEL_PROVIDER` to `dry` and remove the
`GROQ_API_KEY` entry from `render.yaml` in your copy. Push that change to
the branch you will connect before creating the Blueprint.

1. In the Render dashboard, choose **New > Blueprint**. Connect your private
   GitHub copy and select the branch with this `render.yaml`. Before deploying,
   confirm that the preview shows one Docker web service on the **Free** plan.
2. If you are using Groq, enter a key from your Groq Free plan account when
   Render prompts for `GROQ_API_KEY`. Keep the key out of the Dockerfile and Git.
3. Wait for the service to go live. Set `URL` to its HTTPS address, without a
   trailing slash, and run one smoke test:

   ```bash
   URL="https://your-service.onrender.com"
   curl -fsS "$URL/health"
   curl -fsS "$URL/ready"
   curl -fsS "$URL/generate" --json '{"prompt":"Say hello."}'
   ```

   Expect HTTP 200 on all three requests. `/ready` reports the configured
   provider; `/generate` checks that it can return an answer. In dry mode,
   expect `Dry response: Say hello.` and no call to Groq.

Use sample prompts only. The web service is public and has no authentication
or per-client rate limit. Keep live tests brief; use dry mode or add access
controls before sharing the URL. Run the load probe locally. Render and
[Groq](https://console.groq.com/docs/rate-limits) have separate free-tier quotas.
Render can bill build or bandwidth overages if your workspace has a payment
method. Use the local option if you are near a limit.

If you skip hosting, use the [local checks from step 01](01-container-contract.md#verify-the-api)
and the Blueprint table to explain what you would verify on Render.

## Practice

For each verification request, note what an unexpected result would make you
inspect next: the health path, runtime settings, the provider, or input
validation. If you ran a hosted demo, record the deployed revision and label
first-request timings separately from later requests. A slow first request
alone does not identify whether the app, provider, or network caused the wait.
When finished, set `services: []` in your copy of `render.yaml`, push the
change and sync the Blueprint. Then [delete the service in Render](https://render.com/docs/infrastructure-as-code#deleting-resources).
Deleting it before removing it from the Blueprint can cause the next sync to
recreate it.

## Reference Answer

<details>
<summary>Show Reference Answer</summary>

`GROQ_API_KEY` uses `sync: false`, which makes Render request the value during
Blueprint creation. `healthCheckPath: /health` lets Render remove an unhealthy
instance from service without spending tokens on a readiness probe.

</details>

## Check Your Understanding

1. Is a working local container proof of a successful Render deployment?
2. Does the Free Render plan make Groq usage unlimited?

<details>
<summary>Show Reference Answers</summary>

1. No. Verify the deployed routes and runtime configuration separately.
2. No. Render and Groq track usage separately. Dry mode makes no provider calls.

</details>
