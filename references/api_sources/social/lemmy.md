# Lemmy API (Fediverse alternative to Reddit)

## Overview

- **Endpoint base:** Зависит от instance — `https://lemmy.ml/api/v3/` (один из больших)
- **Auth:** None для public read
- **Free tier:** Unlimited (politely)
- **Docs:** https://join-lemmy.org/api/
- **Coverage:** Каждый Lemmy instance свой; популярные: lemmy.ml, lemmy.world, beehaw.org

## Query patterns

### Search posts

```
GET /api/v3/search?q={query}&type_=Posts&sort=TopAll&limit=20
```

### Community posts

```
GET /api/v3/post/list?community_name={community}&sort=Hot&limit=20
```

### Federated search (across instances)

Каждый instance видит federated content — search в lemmy.ml вернёт posts из других инстансов которые он subscribes.

## Use cases

- Альтернативный взгляд на технические темы (когда Reddit cancelled или skews)
- Tech-savvy audience opinions (Lemmy users tend to be technical)
- Decentralized discourse

## Limitations

- Гораздо меньше Reddit
- Coverage uneven — popular topics есть, niche слабее
- Каждый instance — отдельный API endpoint

## Combine with

- **Reddit** — primary social
- **HN** — для tech-specific
- **Mastodon API** — для микроблоггинг alternative

## Notes

- Lemmy всё ещё растёт — useful для тем где Reddit стал toxic или ban-happy
- Полезно для balanced opposition voice
