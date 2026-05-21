# PyPI JSON API

## Overview

- **Endpoint base:** `https://pypi.org/pypi/`
- **Auth:** None
- **Free tier:** Unlimited (politely)
- **Docs:** https://warehouse.pypa.io/api-reference/json.html
- **Coverage:** Все Python packages on PyPI

## Query patterns

### Package metadata

```
GET /pypi/{package_name}/json
# Returns latest version + all versions
```

### Specific version

```
GET /pypi/{package_name}/{version}/json
```

## What it returns

JSON с metadata — name, version, summary, author, dependencies, classifiers, URLs.

```json
{
  "info": {
    "name": "requests",
    "version": "2.31.0",
    "summary": "HTTP for Humans.",
    "author": "Kenneth Reitz",
    "home_page": "https://requests.readthedocs.io",
    "requires_dist": ["charset-normalizer (<4,>=2)", ...],
    "downloads": {...}
  }
}
```

## Use cases

- Find package version, latest release
- Dependency analysis
- Active maintenance signal (last release date)

## Download stats

PyPI JSON doesn't include downloads. Use:

```
GET https://pypistats.org/api/packages/{package}/recent
```

## Limitations

- No search API на этом endpoint — нужен https://pypi.org/search/ scraping или libraries.io
- Download stats отдельный API

## Combine with

- **libraries.io** — для dependency graphs
- **GitHub API** — для repo statistics
- **deps.dev** — Google's deps graph
