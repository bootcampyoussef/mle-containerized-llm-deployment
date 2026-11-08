# Scaling And Failure Diagnosis

The default Blueprint uses one instance to keep the exercise predictable.
`deployment/render.autoscaling.example.yaml` shows the paid autoscaling fields
without enabling them accidentally. Render autoscaling requires a Pro workspace
and bills every active instance.

Compare the example with the main Blueprint. Autoscaling would replace
`numInstances` with the `scaling` block and keep the provider settings and
secret configuration. The workspace subscription and the service's `plan`
(instance size) are separate choices. No scaling change is needed for this lab.

![DistServe goodput chart showing latency constraints as request rate increases](assets/distserve-goodput.png)

*Research context: Figure 1 from [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](https://arxiv.org/abs/2401.09670), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The chart shows why a service can cross a latency target before its raw throughput is exhausted. This repository keeps the implementation on one small container; the figure is here to support the capacity discussion, not as an implementation requirement.*

## Establish A Baseline

Use the healthy dry-mode container from [step 01](01-container-contract.md).
The load probe sends a fixed number of requests, with at most the configured
number in flight **at the client**. That is separate from the API's limit on
concurrent upstream calls.

```bash
uv run --locked python scripts/load_test.py --requests 30 --concurrency 6
```

Expect `successful_requests=30` and `error_rate=0.00%` on a healthy local
run. Timings and request rates depend on the machine. Read the values together:

The probe reuses three prompts, so it measures a cache-heavy workload, not raw
model capacity. p95 uses the nearest-rank definition; transport failures count
as errors rather than aborting the run. Stub-mode timings are not live inference
benchmarks.

`throughput_rps` counts all completed attempts, including failures;
`successful_throughput_rps` counts only 2xx responses. Mean and p95 latency
include failed requests and exclude time waiting for the probe's own semaphore.
A fast failure can improve these timings without improving useful service.
With 30 attempts, nearest-rank p95 is the 29th latency in ascending order.

## Reproduce A Failure

Stop only the Compose service started for this lesson and repeat the same
probe. Restore the baseline afterwards.

```bash
docker compose stop api
uv run --locked python scripts/load_test.py --requests 30 --concurrency 6
MODEL_PROVIDER=dry docker compose up --wait
```

When nothing is listening on port 8000, expect `successful_requests=0` and
`error_rate=100.00%`. The probe counts connection failures even though there
is no HTTP response. `throughput_rps` can still be positive because failed
attempts complete. Verify `/health` again before continuing to the cache lab.

For example, one local run produced:

| API state | Successful requests | Error rate | p95 |
|---|---:|---:|---:|
| Running | 30 | 0% | 10.60 ms |
| Stopped | 0 | 100% | 3.82 ms |

The stopped service looked faster because connections failed quickly. These
timings illustrate the trap; they are not performance targets.

## Practice

Use this observation to separate an unreachable service from a reachable API
that fails upstream. For each symptom below, write down one diagnostic check
and what evidence would justify a change:

- requests end at the platform timeout;
- memory rises until instances restart;
- health checks pass while generation returns `502`; and
- p95 latency rises but CPU remains low.

## Reference Answer

<details>
<summary>Show Reference Answer</summary>

Check queueing and upstream latency first. The application returns `504` when
its total queue-plus-generation deadline expires; other provider failures return
`502`. Smaller workloads or concurrency changes may help; streaming changes
the API contract rather than removing the need for deadlines.
For restarts, check the platform's exit reason and memory graph before assuming
an out-of-memory failure. Passing health with `502` generation responses points
to the provider boundary, not a dead HTTP process. For high latency and low CPU,
separate queue time from upstream time before proposing more replicas. Scaling
the API does not remove an upstream quota, and each replica has its own cache.

</details>

## Check Your Understanding

1. Can a higher total request rate coexist with a complete outage?
2. Does this cache-heavy dry-mode probe measure LLM serving capacity?

<details>
<summary>Show Reference Answers</summary>

1. Yes. Failed requests also complete; inspect successful throughput and error rate.
2. No. It measures this application's stub and cache path, not model inference capacity.

</details>
