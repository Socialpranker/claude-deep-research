# Etherscan API

## Overview

- **Endpoint base:** `https://api.etherscan.io/api`
- **Auth:** API key (query param `apikey`)
- **Free tier:** 5 req/sec, 100k req/day
- **Paid:** custom plans
- **Docs:** https://docs.etherscan.io
- **Coverage:** Ethereum mainnet (similar APIs для других chains)

## Sister APIs (same structure)

- **BSCScan:** api.bscscan.com — Binance Smart Chain
- **Polygonscan:** api.polygonscan.com — Polygon
- **Arbiscan:** api.arbiscan.io — Arbitrum
- **Optimistic Etherscan:** api-optimistic.etherscan.io — Optimism
- **Basescan:** api.basescan.org — Base

## Auth setup

1. https://etherscan.io/myapikey → free key
2. `export ETHERSCAN_KEY="..."`

## Query patterns

### Account balance

```
GET /api?module=account&action=balance&address=0x...&tag=latest&apikey={key}
```

### Transaction list

```
GET /api?module=account&action=txlist&address=0x...&startblock=0&endblock=99999999&sort=desc&apikey={key}
```

### Contract source

```
GET /api?module=contract&action=getsourcecode&address=0x...&apikey={key}
```

### Token transfers

```
GET /api?module=account&action=tokentx&address=0x...&apikey={key}
```

### Token info (ERC-20)

```
GET /api?module=token&action=tokeninfo&contractaddress=0x...&apikey={key}
```

## Use cases

- Wallet activity analysis
- Smart contract verification
- Token holder distribution
- Transaction pattern analysis

## Limitations

- Ethereum only (sister chains have separate APIs)
- 100k/day хватает большинству, но heavy analytics нужен paid
- Pricing data слабее чем у CoinGecko

## Combine with

- **DefiLlama** — для protocol-level metrics
- **Dune Analytics** — для custom SQL queries on-chain
- **CoinGecko** — для token prices
