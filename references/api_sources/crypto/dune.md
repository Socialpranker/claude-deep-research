# Dune Analytics API

## Overview

- **Endpoint base:** `https://api.dune.com/api/v1/`
- **Auth:** API key
- **Free tier:** 1000 datapoints/month
- **Paid:** $390/mo для Pro
- **Docs:** https://dune.com/docs/api/
- **Coverage:** Custom SQL queries on Ethereum, Polygon, Solana, Bitcoin, etc.

## Auth setup

1. https://dune.com → register, upgrade
2. API key из settings
3. `export DUNE_API_KEY="..."`

## Query patterns

### Execute query (existing)

```
POST /query/{query_id}/execute
Headers: x-dune-api-key: {key}
```

### Get results

```
GET /execution/{execution_id}/results
```

### Get pre-computed query latest results

```
GET /query/{query_id}/results
```

## Use cases

- Custom on-chain metrics (что нет в готовых APIs)
- Cross-chain comparisons
- Wallet behavior analysis
- DEX/CEX volume analytics

## Limitations

- **Expensive** для production
- Requires SQL knowledge для creating queries
- Best — reuse existing public queries (Dune community shares 10k+ dashboards)

## Workflow

1. Найти public Dune dashboard по теме: https://dune.com/browse/dashboards
2. Извлечь query ID
3. Execute via API
4. Save results к sources/NN.md

## Combine with

- **DefiLlama** — для standardized metrics
- **Etherscan** — для raw on-chain
- **Glassnode** — для BTC/ETH macro
