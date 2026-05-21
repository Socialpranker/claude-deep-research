# Currents API

## Overview

- **Endpoint base:** `https://api.currentsapi.services/v1/`
- **Auth:** API key
- **Free tier:** 600 requests/day
- **Docs:** https://currentsapi.services/en/docs/
- **Coverage:** Global news, 60+ countries, 35+ languages

## Auth setup

1. https://currentsapi.services/en/register → free key
2. `export CURRENTS_API_KEY="..."`

## Query patterns

### Latest news

```
GET /latest-news?apiKey={key}&language=en&keywords={query}
```

### Search

```
GET /search?apiKey={key}&keywords={query}&category=technology&country=us&start_date=2024-01-01
```

## Use cases

- Alternative to NewsAPI с лучшим free tier
- Multi-language coverage
- Category filtering

## Limitations

- Меньше известный, sources catalog меньше
- Quality varies

## Combine with

- **NewsAPI** — primary
- **GDELT** — для macro tracking
- **Direct RSS feeds**
