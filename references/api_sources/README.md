# API sources — README

Как пользоваться API каталогом.

## Шаблон файла API (для каждой записи)

```markdown
# <API Name>

## Overview

- **Endpoint base:** `https://api.example.com/v2/`
- **Auth:** none / API key / OAuth / Bearer token
- **Free tier:** 100 req/day / unlimited / N/A
- **Rate limit:** 10 req/sec
- **Docs:** `https://docs.example.com`
- **Status page:** `https://status.example.com`

## What it returns

Структурированный JSON. Пример response для типового запроса.

## When to use

- Use case 1
- Use case 2

## When not to use

- Edge case where this is wrong choice

## Auth setup

Если нужен ключ — где взять, какие пермишены.

## Query patterns

### Search/lookup
\`\`\`
GET /v2/search?q={query}&limit=20
\`\`\`

### Bulk
\`\`\`
POST /v2/bulk
Body: { "ids": [...] }
\`\`\`

## Example queries

Конкретные queries с примерами JSON response (truncated).

## Limitations

- Geographic coverage
- Data lag (real-time / 1 day / 1 week)
- Missing fields
- Known issues

## Combine with

- Related APIs to triangulate
- Related HTML sources in `stat_sources/` for fallback

## Fallback if API down or rate-limited

1. Cached responses (if any)
2. Alternative API
3. HTML source from `stat_sources/`
```

## Auth strategy для агента

Скилл **не хранит ключи**. Когда агенту нужен API с ключом:

1. **Сначала** проверить переменные окружения:
   - `FRED_API_KEY`, `GITHUB_TOKEN`, `NEWSAPI_KEY`, `BRAVE_API_KEY`, etc.
2. Если ключа нет → fallback на free версию (без auth) или на HTML source
3. **Никогда** не запрашивать у пользователя ключ inline — попросить добавить в env и перезапустить

Пример agent prompt:

```
Я попробую использовать FRED API. Проверяю $FRED_API_KEY...
Не найден → fallback на HTML парсинг fred.stlouisfed.org через WebFetch.

Чтобы ускорить будущие ресёрчи с FRED:
1. Получи бесплатный ключ: https://fred.stlouisfed.org/docs/api/api_key.html
2. Добавь в ~/.zshrc или ~/.bashrc:
   export FRED_API_KEY="your-key-here"
3. Перезапусти shell и Claude Code
```

## Free tier dispatch logic

```
если нужен API X:
  если есть API key в env:
    → используй API
  иначе если есть free tier без key:
    → используй free tier
  иначе:
    → fallback на HTML версию из stat_sources/<category>.md
    → отметь в sources/NN.md: access: html-fallback (api blocked)
```

## Rate limit handling

При попадании на 429 (rate limit):

1. Подожди время указанное в `Retry-After` header
2. Если ждать > 30 сек → fallback на HTML или альтернативный API
3. Отметь в `sources/NN.md` notes: `rate-limited at <timestamp>, fell back to <source>`

## API quality grading

В `sources/NN.md` для API-полученных источников:

- `channel: api-direct`
- `access:` одно из:
  - `api-free-no-key` — лучший вариант
  - `api-free-with-key` — потребует setup но free
  - `api-paid` — платный, использовали потому что free не покрыл
  - `api-fallback-html` — API не работал, fall back на HTML

## Когда добавлять новый API в каталог

Критерии для PR:

- API стабильно работает >1 года
- Имеет официальную документацию
- Имеет free tier ИЛИ закрывает unique gap (нет free альтернативы)
- Возвращает структурированный JSON/XML
- Не deprecated и не "beta" с агрессивными breaking changes

## Антипаттерны

- ❌ Документировать API без проверки что он работает
- ❌ Игнорировать rate limits — нужно знать пределы
- ❌ Хардкодить ключи в шаблонах queries — всегда через env
- ❌ Дублировать stat_sources/ — API запись должна давать качественное другое (программный access), не просто другой URL
- ❌ Добавлять API без fallback стратегии
