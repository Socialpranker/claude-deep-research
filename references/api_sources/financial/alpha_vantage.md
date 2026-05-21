# Alpha Vantage

## Overview

- **Endpoint base:** `https://www.alphavantage.co/query`
- **Auth:** API key (query param `apikey`)
- **Free tier:** 25 requests/day (limited!), 5 calls/min
- **Paid:** $50/mo для 75 requests/min, $250/mo unlimited
- **Docs:** https://www.alphavantage.co/documentation/
- **Coverage:** Stocks, forex, crypto, commodities, technical indicators

## Auth setup

1. https://www.alphavantage.co/support/#api-key → free key
2. `export ALPHA_VANTAGE_KEY="..."`

## Query patterns

### Stock daily

```
GET /query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={key}
```

### Forex

```
GET /query?function=FX_DAILY&from_symbol=USD&to_symbol=EUR&apikey={key}
```

### Crypto

```
GET /query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={key}
```

### Company overview

```
GET /query?function=OVERVIEW&symbol=AAPL&apikey={key}
```

## Limitations

- **25 req/day** на free tier — реально мало для активного использования
- Free tier — для validation, не для production

## Combine with

- **SEC EDGAR** — для US public companies (бесплатно, unlimited)
- **Yahoo Finance** — fallback на price data через scraping
- **FRED** — для macro context

## Fallback

- Yahoo Finance API (unofficial endpoints)
- Stooq.com (free historical data)
- Manually WebFetch finance.yahoo.com pages
