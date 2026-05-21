# Stack Exchange API

## Overview

- **Endpoint base:** `https://api.stackexchange.com/2.3/`
- **Auth:** App key (optional, без него работает)
- **Free tier:** 300 req/day без key, 10000 req/day с key
- **Docs:** https://api.stackexchange.com/docs
- **Coverage:** Stack Overflow + 170 sister sites (DBA, Math, etc.)

## Auth setup (optional but recommended)

1. https://stackapps.com/apps/oauth/register
2. Получи `key` (app key, не secret)
3. `export STACKEXCHANGE_KEY="..."`

## Query patterns

### Search questions

```
GET /search?intitle={query}&site=stackoverflow&order=desc&sort=relevance&key={STACKEXCHANGE_KEY}
```

### Question + answers

```
GET /questions/{id}?site=stackoverflow&filter=withbody&key={STACKEXCHANGE_KEY}
```

### Tag-filtered search

```
GET /search/advanced?q={query}&tagged=python+pandas&site=stackoverflow&order=desc&sort=votes
```

## Use cases

- Поиск решённых проблем
- Find community sentiment on technology choices
- Understand common pitfalls (look at upvoted answers about errors)

## Sites available

- `stackoverflow` — general programming
- `superuser` — power user
- `serverfault` — sysadmins
- `dba` — databases
- `math` — math
- `stats` — statistics
- `tex` — LaTeX
- `english` — language Q&A

## Limitations

- 300 req/day без key — для серьёзного use нужен key
- Search relevance не всегда отличный — нужно проверять
