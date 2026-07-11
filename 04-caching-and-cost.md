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

The second identical request is served from cache and reports zero incremental
provider cost. Temperature belongs in the cache key because it can change the
output. A monthly estimate must separate fixed instance hours from variable
provider usage and state the assumed cache-hit rate.
