# Caching And Cost

The service reports token usage, estimated cost, latency, and cache status.
Pricing is configuration because provider rates change; copy current rates from
the provider's pricing page into `.env` before making a cost claim.

## Follow A Cache Miss And Hit

Use the dry-mode service from step 03. Pick a prompt you have not used during
this run, and send it twice within the cache TTL (300 seconds by default).

```bash
for attempt in 1 2; do
  curl -sS http://127.0.0.1:8000/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Describe the cache experiment.","temperature":0.2}'
  printf '\n'
done
```

Expect `cache_hit: false` then `cache_hit: true`. The second request returns
the stored text and its original token counts, but no new provider call.
`estimated_cost_usd` is zero on a hit; both responses can show zero with the
default unconfigured prices. A faster second response is useful evidence, but
the cache flag is the direct check.

The [cache key](src/deployment_service/cache.py) includes the configured model,
prompt, token limit, and temperature. Try the same request with
`"temperature":0.5`: expect a miss if you have not sent that combination.
Restarting the process clears the cache. It is not shared between replicas.

## Work Through A Cost Estimate

Separate fixed instance cost from variable provider cost. Suppose a service
handles 2,000 successful requests per month and 80% are cache hits. That leaves
400 generations under this simplified assumption. With 100 input and 50
output tokens per generation, and **illustrative** prices of $1 and $3 per
million tokens respectively:

```text
provider cost = 400 * (100 * 1 + 50 * 3) / 1,000,000 = $0.10
total estimate = instance cost + provider cost
```

This is not a quote or bill. Measure real provider usage on a defined workload
and look up the relevant prices before using the estimate for a decision.

## Practice

Compare the cost and failure impact of adding a second replica versus keeping
one replica and improving the cache-hit rate. Use your observed cache flags
and the failure probe, and state what evidence is still missing. A local stub
cannot tell you the live provider's capacity or your production cache-hit rate.

## Reference Answer

<details>
<summary>Show Reference Answer</summary>

The second identical request is served from cache and reports zero incremental
provider cost. Temperature belongs in the cache key because it can change the
output. A monthly estimate must separate fixed instance hours from variable
provider usage and state the assumed cache-hit rate.

The cache is process-local, capped at 1,024 entries, and cleared on restart.
Instances do not share it, and simultaneous misses can still call the provider
more than once. Returned token counts describe the cached answer; only the
incremental cost is zero on a hit. In stub mode, token counts are word-count
estimates, not model tokenizer measurements.

Stub responses identify their model with a `dry:` prefix. Their estimated cost
is a simulation; default prices of zero mean pricing is not configured, not
that live inference is free.

</details>

## Clean Up

```bash
docker compose down
```

This stops and removes the lesson's Compose containers and network. The image
remains available for reuse. Hosted resources must be removed separately.

## Check Your Understanding

1. Does a cache hit imply that no tokens were used to create the answer?
2. Does a zero token-price setting make a live provider free?

<details>
<summary>Show Reference Answers</summary>

1. No. It avoids a new provider call; the original generation still used tokens.
2. No. Zero means no price is configured in the estimator, not that billing is disabled.

</details>
