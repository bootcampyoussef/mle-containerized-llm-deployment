# Caching And Cost

The service reports token usage, estimated cost, latency, and cache status.
Pricing is configuration because provider rates change; copy current rates from
the provider's pricing page into `.env` before making a cost claim.

## Practice

Send the same request twice and compare `cache_hit`, `latency_ms`, and
`estimated_cost_usd`. Then change only the temperature and explain the result.
Estimate monthly cost for your measured request volume, cache-hit rate, and
Render instance plan.

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

## Check Your Understanding

1. Does a cache hit imply that no tokens were used to create the answer?
2. Does a zero token-price setting make a live provider free?

<details>
<summary>Show Reference Answers</summary>

1. No. It avoids a new provider call; the original generation still used tokens.
2. No. Zero means no price is configured in the estimator, not that billing is disabled.

</details>
