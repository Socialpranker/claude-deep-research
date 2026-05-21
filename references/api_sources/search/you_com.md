# You.com Search API

## Overview

- **Endpoint base:** `https://api.ydc-index.io`
- **Auth:** API key (header `X-API-Key`)
- **Free tier:** 1000 requests / month
- **Paid:** custom pricing
- **Docs:** https://documentation.you.com
- **Unique:** AI-optimized search with snippets ready for LLM context

## What it returns

JSON с web/news/snippets specifically formatted for LLM consumption.

```json
{
  "hits": [
    {
      "title": "...",
      "url": "...",
      "snippets": [
        "snippet 1 ready for LLM context...",
        "snippet 2..."
      ],
      "description": "...",
      "thumbnail_url": "..."
    }
  ]
}
```

## When to use

- Need LLM-ready snippets (no need to re-process)
- Alternative when Tavily/Brave free tier exhausted
- News-heavy queries

## When not to use

- Если уже используешь Tavily/Brave и они работают — switching не даст ценности
- Простой WebSearch достаточно

## Auth setup

1. https://api.you.com → register
2. API key из dashboard
3. В env: `export YOU_API_KEY="..."`

## Query patterns

### Web search

```
GET https://api.ydc-index.io/search?query={query}&num_web_results=10
Headers: X-API-Key: {YOU_API_KEY}
```

### News search

```
GET https://api.ydc-index.io/news?query={query}&num_news_results=10
Headers: X-API-Key: {YOU_API_KEY}
```

### Search with country/language

```
GET /search?query={query}&country=US&safesearch=moderate
```

## Limitations

- Index не настолько богат как Google/Brave для нишевых тем
- Free tier 1000/mo
- Меньше features чем SerpAPI

## Combine with

- **Tavily** — primary AI-focused search
- **Brave Search** — для broader coverage
- **You.com** — backup или specific use cases

## Fallback if API down or rate-limited

1. Tavily
2. Brave Search
3. Standard WebSearch
