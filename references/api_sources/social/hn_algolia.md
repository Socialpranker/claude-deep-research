# Hacker News Algolia API

## Overview

- **Endpoint base:** `https://hn.algolia.com/api/v1/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** https://hn.algolia.com/api
- **Coverage:** Все HN posts + comments since 2007

## Query patterns

### Search

```
GET /search?query={query}&tags=story&hitsPerPage=50
```

### Search recent

```
GET /search_by_date?query={query}&tags=story&numericFilters=created_at_i>{timestamp}
```

### Filter by tags

- `story`, `comment`, `poll`, `pollopt`
- `front_page` — was on HN front page
- `author_{username}`
- `story_{id}` — comments on specific story

### Specific item

```
GET /items/{id}
```

## Use cases

- Tech industry sentiment
- Find seminal posts (HN often surfaces them)
- Expert opinions (тech founders, engineers активно postят)
- Validate technology adoption narrative

## Example queries

**Phase 4 — tech opinion landscape:**

```
GET /search?query=polymarket&tags=story&hitsPerPage=50
```

**Phase 4 — recent only:**

```
GET /search_by_date?query=prediction+markets&tags=story&numericFilters=created_at_i>1704067200
```

## Limitations

- HN audience skews technical + libertarian — bias в opinions
- Comments длинные threads — нужна обработка hierarchy

## Combine with

- **Reddit** — для broader community
- **Twitter** — для real-time
- **GitHub** — для actual implementation

## Notes

- Один из самых надёжных social APIs — Algolia maintains stable infrastructure
- Excellent для tech topics, weak для не-tech
