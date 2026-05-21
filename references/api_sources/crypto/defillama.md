# DefiLlama API

## Overview

- **Endpoint base:** `https://api.llama.fi`
- **Auth:** None
- **Free tier:** Unlimited (politely)
- **Docs:** https://defillama.com/docs/api
- **Coverage:** 3000+ DeFi protocols, all major chains, stablecoins

## Query patterns

### All protocols

```
GET /protocols
```

### Protocol details

```
GET /protocol/{slug}
# Example: /protocol/aave-v3
```

### Total TVL

```
GET /tvl/{protocol-slug}
```

### Chains TVL

```
GET /chains
```

### Stablecoins

```
GET /stablecoins
GET /stablecoincharts/all
```

### Yields

```
GET /pools  # via api.llama.fi-yields
```

## Use cases

- DeFi protocol analysis
- Chain ecosystem comparison (TVL by chain)
- Stablecoin tracking
- Yield farming opportunities

## Limitations

- Только DeFi (NFT/gaming не покрыты)
- Self-reported TVL — некоторые protocols inflate

## Combine with

- **CoinGecko** — для token prices
- **Dune Analytics** — для custom on-chain queries
- **Etherscan** — для contract-level details
