# npm Registry API

## Overview

- **Endpoint base:** `https://registry.npmjs.org/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
- **Coverage:** Все npm packages

## Query patterns

### Package metadata

```
GET /{package}
# Returns all versions, dependencies, maintainers
```

### Specific version

```
GET /{package}/{version}
```

### Search

```
GET https://registry.npmjs.org/-/v1/search?text={query}&size=20
```

### Download stats

```
GET https://api.npmjs.org/downloads/range/last-month/{package}
GET https://api.npmjs.org/downloads/point/last-week/{package}
```

## Use cases

- Find package version, dependencies
- Active maintenance signal (last publish date)
- Downloads trend — for tech adoption analysis

## Limitations

- Search relevance variable
- Some packages have download spikes от bots

## Combine with

- **deps.dev** (Google) — для security + advanced graph
- **libraries.io** — для cross-ecosystem
- **GitHub API** — для repo source
