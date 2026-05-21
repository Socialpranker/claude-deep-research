# World Bank Indicators API

## Overview

- **Endpoint base:** `https://api.worldbank.org/v2/`
- **Auth:** None
- **Free tier:** Unlimited
- **Rate limit:** soft, polite usage expected
- **Docs:** https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- **Coverage:** 16k+ indicators across 217 countries, 50+ years

## What it returns

JSON или XML — time series по indicator × country.

```json
[{"page": 1, "pages": 1, "per_page": 50, "total": 30},
 [{"indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
   "country": {"id": "US", "value": "United States"},
   "value": 27360935000000, "date": "2023"},
  ...]]
```

## Query patterns

### Country data

```
GET /country/US/indicator/NY.GDP.MKTP.CD?format=json&date=2000:2024
```

`NY.GDP.MKTP.CD` = GDP в текущих $. Indicator IDs: https://data.worldbank.org/indicator

### Multiple countries

```
GET /country/US;CN;RU;DE/indicator/SP.POP.TOTL?format=json&date=2020:2024
# Population for 4 countries
```

### All countries one indicator

```
GET /country/all/indicator/NY.GDP.MKTP.CD?format=json&date=2023&per_page=300
```

### Common indicator IDs

- `NY.GDP.MKTP.CD` — GDP (current US$)
- `SP.POP.TOTL` — Population
- `SI.POV.GINI` — Gini index
- `SE.XPD.TOTL.GD.ZS` — Education spending % GDP
- `EN.ATM.CO2E.PC` — CO2 emissions per capita
- `IT.NET.USER.ZS` — Internet users %
- `FP.CPI.TOTL.ZG` — Inflation %

## Example queries

**Country macro snapshot:**

```
GET /country/RU/indicator/NY.GDP.MKTP.CD;FP.CPI.TOTL.ZG;SL.UEM.TOTL.ZS?format=json&date=2020:2024
```

## Limitations

- 1-2 year lag для большинства indicators
- Coverage слабая для small/developing countries
- Не real-time

## Combine with

- **FRED** — для US детали (быстрее обновляется)
- **OECD** — для developed countries
- **IMF API** — для finance/balance of payments

## Fallback

- HTML scrape data.worldbank.org
- OWID (`ourworldindata.org`) — curated subset с visualizations
