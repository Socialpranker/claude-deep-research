# NewsAPI.org

## Overview

- **Endpoint base:** `https://newsapi.org/v2/`
- **Auth:** API key
- **Free tier:** 100 req/day, articles from last month only
- **Paid:** $449/mo для unlimited + full archive
- **Docs:** https://newsapi.org/docs
- **Coverage:** 150k+ sources, 50+ countries

## Auth setup

1. https://newsapi.org/register → free key
2. `export NEWSAPI_KEY="..."`

## Query patterns

### Top headlines

```
GET /top-headlines?country=us&category=business&apiKey={key}
```

### Everything (broad search)

```
GET /everything?q={query}&from=2024-01-01&to=2024-12-31&sortBy=relevancy&apiKey={key}
```

### Sources

```
GET /sources?category=technology&language=en&country=us&apiKey={key}
```

## Use cases

- Current events lookup
- Recent news context для landscape research
- Track narrative over time

## Limitations

- Free tier — только последний месяц
- 100 req/day мало для активного use
- Coverage не uniform — некоторые sources обновляются медленно

## Combine with

- **GDELT** — free, broader coverage, sentiment
- **Currents API** — free alternative
- **Direct RSS feeds** specific outlets
