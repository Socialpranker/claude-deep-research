# Reddit JSON API

## Overview

- **Endpoint base:** `https://www.reddit.com/`
- **Auth:** None для public read
- **Free tier:** ~100 req/min (sometimes blocked)
- **Note:** Set User-Agent в headers — без него blocked
- **Docs:** https://www.reddit.com/dev/api/ (older Reddit OAuth API более стабильный)
- **Coverage:** Все public subreddits + posts + comments

## What it returns

JSON — просто добавь `.json` к URL Reddit page.

## Required headers

```
User-Agent: deep-research-skill/1.0 (your-contact)
```

Без этого Reddit блокирует.

## Query patterns

### Subreddit posts

```
GET https://www.reddit.com/r/{subreddit}/hot.json?limit=25
GET https://www.reddit.com/r/{subreddit}/top.json?t=year&limit=25
# t=hour/day/week/month/year/all
```

### Search

```
GET https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&sort=relevance
GET https://www.reddit.com/search.json?q={query}&sort=relevance
```

### Post with comments

```
GET https://www.reddit.com/r/{subreddit}/comments/{id}.json?limit=100
```

### User profile

```
GET https://www.reddit.com/user/{username}/submitted.json
GET https://www.reddit.com/user/{username}/comments.json
```

## Use cases

- Community sentiment
- Opposition research (find critical posts)
- Anecdotal experiences ("my experience with X")
- Real-world implementation pitfalls

## Example queries для deep-research

**Phase 4 — community opposition:**

```
GET https://www.reddit.com/r/Polymarket/search.json?q=lost+money&restrict_sr=1&sort=relevance&limit=50
```

**Phase 4 — broad search:**

```
GET https://www.reddit.com/search.json?q=polymarket+market+maker+experience&sort=top&t=year
```

## Limitations

- Blocking aggressive — easy to get rate-limited
- Some subreddits private/blocked
- Vote manipulation existed historically — sentiment не идеален
- Old Reddit format slightly different

## Combine with

- **HN Algolia** — для tech-specific discussion
- **Twitter** (если есть access)
- **Forum search** general via Brave/Tavily

## Fallback

- OAuth Reddit API (более стабильный с rate limits)
- Direct WebFetch с good User-Agent
- Pushshift.io (archive, sometimes works)

## Notes

- `.json` после любого Reddit URL работает — это самый простой research API в мире
- Хорошо для opposition voice в phase 4 (counter-arguments)
- Reddit search relevance плохой — лучше Brave/SerpAPI с `site:reddit.com`
