# Eurostat REST API

## Overview

- **Endpoint base:** `https://ec.europa.eu/eurostat/api/dissemination/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started
- **Coverage:** Все EU statistics — demographics, economy, environment, etc.

## Query patterns

### Get dataset (JSON-stat format)

```
GET /statistics/1.0/data/{dataset_code}?format=JSON&time=2023&geo=DE,FR,IT
```

Find dataset codes: https://ec.europa.eu/eurostat/data/database

### Common datasets

- `prc_hicp_manr` — Inflation HICP
- `une_rt_m` — Unemployment monthly
- `nama_10_gdp` — GDP
- `migr_pop1ctz` — Migration
- `sdg_*` — Sustainable Development Goals

## Use cases

- EU macro economics
- Cross-country EU comparisons
- Eurozone-specific indicators

## Limitations

- JSON-stat format awkward для агента (требует parsing dimensions)
- 1-2 month lag на most indicators

## Combine with

- **ECB** — для finance specifics
- **World Bank** — для broader context
- **FRED** — для US comparison
