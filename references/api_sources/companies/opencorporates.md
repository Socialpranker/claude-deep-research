# OpenCorporates API

## Overview

- **Endpoint base:** `https://api.opencorporates.com/v0.4/`
- **Auth:** None для basic (premium token для бóльшего)
- **Free tier:** 500 req/day анонимно, 50/мин
- **Paid:** Free для journalists/researchers, paid для commercial
- **Docs:** https://api.opencorporates.com
- **Coverage:** 200M+ companies из company registries 130+ countries

## What it returns

JSON с данные из официальных company registries — incorporation date, officers, addresses, filings.

```json
{
  "results": {
    "company": {
      "name": "Apple Inc.",
      "company_number": "C0806592",
      "jurisdiction_code": "us_ca",
      "incorporation_date": "1977-01-03",
      "officers": [...],
      "registered_address": {...}
    }
  }
}
```

## Query patterns

### Search companies

```
GET /companies/search?q={query}&country_code=US&per_page=20
```

### Company details

```
GET /companies/{jurisdiction}/{company_number}
# Example: /companies/us_ca/C0806592 (Apple)
```

### Officer search

```
GET /officers/search?q={name}&per_page=20
```

## Use cases

- Find official company existence (vs marketing claims)
- Track officer/director relationships
- Verify incorporation dates
- Find parent companies, subsidiaries

## Limitations

- Не финансовые данные — только registry facts
- Coverage uneven — UK/EU strong, US weaker (state-level)
- Some jurisdictions lag

## Combine with

- **Crunchbase** — для funding history
- **Companies House** (UK) — больше деталей для UK
- **SEC EDGAR** — для US public companies

## Fallback

- Direct national registries (Companies House, Bundesanzeiger, etc.)
- HTML scraping company official pages
