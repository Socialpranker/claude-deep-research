# Crunchbase Basic API

## Overview

- **Endpoint base:** `https://api.crunchbase.com/api/v4/`
- **Auth:** API key (query param `user_key`)
- **Free tier:** Trial only, then paid
- **Paid:** $99/mo Basic, scales up
- **Docs:** https://data.crunchbase.com/docs/getting-started
- **Coverage:** Startup data — funding rounds, founders, acquisitions, valuations

## What it returns

JSON с organization data, funding events, people, news.

## Auth setup

1. https://www.crunchbase.com/api → request
2. `export CRUNCHBASE_API_KEY="..."`

## Query patterns

### Organization details

```
GET /entities/organizations/{uuid}?field_ids=name,short_description,founded_on,total_funding_amount&user_key={key}
```

### Search organizations

```
POST /searches/organizations
Body: {
  "query": [{"type": "predicate", "field_id": "industries", "operator_id": "includes", "values": ["fintech"]}],
  "field_ids": ["name", "short_description", "total_funding_amount"],
  "limit": 50
}
```

### Funding rounds

```
GET /entities/funding_rounds/{uuid}
```

## Example queries для deep-research

**Phase 4 — competitive landscape:**

```
POST /searches/organizations
{
  "query": [
    {"type": "predicate", "field_id": "industries", "operator_id": "includes", "values": ["prediction markets"]},
    {"type": "predicate", "field_id": "founded_on", "operator_id": "gte", "values": ["2018-01-01"]}
  ],
  "field_ids": ["name", "total_funding_amount", "investor_identifiers", "founded_on"],
  "limit": 50
}
```

## Limitations

- **Paid** для серьёзного использования
- Free trial expires
- Data quality лучше для US/EU startups, слабее для Asia

## Combine with

- **OpenCorporates** — для company registry data (free)
- **PitchBook** — alternative (paid, comprehensive)
- **AngelList/Wellfound** — для startup jobs

## Fallback

- HTML scrape Crunchbase profiles
- Latka SaaS revenue database
- Company's own about page + LinkedIn
