# Crypto / Web3

On-chain data, DeFi, crypto markets. Уникально верифицируемая категория — большая часть данных on-chain и cross-checkable.

## Markets / Prices

### CoinGecko
**URL:** coingecko.com/en/coins/<coin>
**Access:** OPEN
**What:** Full crypto market data — price, volume, mcap, supply, historical. 10k+ tokens. API free with rate limits.
**When:** crypto market sizing, price history, comparing tokens
**Quality:** A — aggregator of exchanges, verifiable on-chain
**How:** Direct URL or API; `coingecko.com/api/documentation`
**Combine with:** CoinMarketCap (cross-check)

### CoinMarketCap
**URL:** coinmarketcap.com/currencies/<coin>
**Access:** OPEN
**What:** Same as CoinGecko, slightly different methodology
**When:** cross-check CoinGecko numbers
**Quality:** A
**Owned by:** Binance — minor bias possible toward Binance-listed tokens

### TradingView Crypto
**URL:** tradingview.com/markets/cryptocurrencies/
**Access:** OPEN (free tier)
**What:** Charts, technical analysis tools, screeners
**When:** technical analysis, charting

## On-chain analytics

### DefiLlama
**URL:** defillama.com
**Access:** OPEN
**What:** TVL (Total Value Locked) per DeFi protocol, chain, category. Stablecoins data. Yields. API free.
**When:** DeFi protocol comparison, chain ecosystem analysis, TVL claims
**Quality:** A — on-chain derived
**How:** Browse by chain/protocol; API `api.llama.fi`
**Combine with:** Dune Analytics, project's own docs

### Dune Analytics
**URL:** dune.com
**Access:** OPEN (community dashboards)
**What:** SQL-based on-chain analytics, community-built dashboards (millions of queries)
**When:** custom on-chain metrics, специальные analyses (NFT sales, DEX volumes, etc)
**Quality:** A (raw on-chain), but dashboard quality varies — check builder reputation
**How:** Browse public dashboards; search by topic; `dune.com/browse`

### Etherscan / equivalent
**URL:** etherscan.io (Ethereum), bscscan.com (BSC), polygonscan.com (Polygon), arbiscan.io (Arbitrum), basescan.org (Base)
**Access:** OPEN
**What:** Block explorers — transactions, contracts, addresses, token transfers
**When:** specific transaction analysis, wallet activity, contract verification
**Quality:** A — direct on-chain

### Glassnode
**URL:** glassnode.com/insights
**Access:** PARTIAL (insights free, full data paywall)
**What:** Bitcoin & Ethereum on-chain metrics — HODLer behavior, exchange flows, miner data
**When:** BTC/ETH macro analysis
**Quality:** A
**Insights blog:** free, very useful

### Nansen
**URL:** nansen.ai
**Access:** PARTIAL
**What:** Wallet labels, smart money tracking
**When:** smart money flow analysis

### Token Terminal
**URL:** tokenterminal.com
**Access:** PARTIAL
**What:** Protocol financials — revenue, P/S ratio, treasury
**When:** treating DeFi protocols как companies

## Specific ecosystems

### L2BEAT
**URL:** l2beat.com
**Access:** OPEN
**What:** Ethereum L2 ecosystem — TVL, risk, technology breakdown
**When:** L2 comparison, rollup analysis
**Quality:** A — independent, well-respected

### Messari
**URL:** messari.io
**Access:** PARTIAL (research free, pro paywall)
**What:** Crypto research, project profiles, news
**When:** project deep-dives

### The Block
**URL:** theblock.co
**Access:** OPEN articles, paywall pro research
**What:** Crypto news with data + research reports
**When:** news context + landscape data

### DappRadar
**URL:** dappradar.com
**Access:** OPEN
**What:** dApp rankings, NFT marketplace data, gamefi
**When:** specific dApp metrics

## NFT-specific

- **OpenSea** stats — opensea.io/rankings — OPEN
- **CryptoSlam** — cryptoslam.io — OPEN NFT sales rankings
- **NFTGo** — nftgo.io — OPEN analytics
- **CryptoArt.io** — partial

## Exchange-specific

- **CoinDesk Indices** — coindesk.com/indices — institutional indices
- **CryptoCompare** — cryptocompare.com — alternative aggregator
- **Kaiko** — partial paid data
- **Coinmetrics** — coinmetrics.io — Network data, free + paid tiers

## Quick reference

| Что ищем | Источник |
|---|---|
| Token price/mcap | CoinGecko + CoinMarketCap |
| DeFi protocol TVL | DefiLlama |
| Custom on-chain metric | Dune Analytics |
| Wallet/contract details | Etherscan (or chain equivalent) |
| BTC/ETH macro signals | Glassnode insights |
| L2 ecosystem | L2BEAT |
| NFT sales | CryptoSlam + OpenSea |
| Protocol revenue | Token Terminal |
| Smart money tracking | Nansen |

## Critical reminders

- **On-chain = verifiable.** Это уникальное преимущество crypto data. Большинство claims проверяемы independently.
- **Aggregator vs source.** CoinGecko aggregates exchanges — может быть wrong для thin markets. Always check на specific exchange.
- **Wash trading.** Volume claims часто inflated через wash trades. Check Bitwise reports о real volume.
- **Self-reported metrics** (project's own dashboards) — bias toward favorable framing.

## Combining patterns

**DeFi protocol analysis:**
DefiLlama (TVL) + Dune (custom metrics) + Token Terminal (revenue) + project docs + Etherscan (contract audit)

**Token investment due diligence:**
CoinGecko (market data) + on-chain explorer (top holders) + Dune (custom queries) + project's GitHub (development activity) + community forums (sentiment)

**Crypto market overview:**
CoinGecko (top tokens) + DefiLlama (DeFi state) + L2BEAT (L2 share) + Messari research (narratives) + Glassnode (BTC dominance)
