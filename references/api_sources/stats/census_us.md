# US Census Bureau API

## Overview

- **Endpoint base:** `https://api.census.gov/data/`
- **Auth:** API key (recommended)
- **Free tier:** Unlimited with key, 500 req/day без key
- **Docs:** https://www.census.gov/data/developers/data-sets.html
- **Coverage:** US demographics, business, housing, economic indicators

## Auth setup

1. https://api.census.gov/data/key_signup.html → free key (instant)
2. `export CENSUS_API_KEY="..."`

## Query patterns

### ACS (American Community Survey)

```
GET /2022/acs/acs5?get=NAME,B01003_001E&for=state:*&key={key}
# Population by state
```

### Decennial Census

```
GET /2020/dec/pl?get=NAME,P1_001N&for=county:*&in=state:06&key={key}
# Population by county in California
```

### Economic Census

```
GET /2017/ecnbasic?get=NAICS2017,ESTAB&for=state:06&key={key}
```

## Useful datasets

- `acs/acs5` — ACS 5-year estimates (most reliable)
- `acs/acs1` — ACS 1-year (large geos only)
- `dec/pl` — Decennial PL data
- `pep/population` — Population estimates
- `ecnbasic` — Economic Census basic
- `cbp` — County Business Patterns
- `bds` — Business Dynamics Statistics

## Variable lookup

https://api.census.gov/data/2022/acs/acs5/variables.html

## Limitations

- Variable naming difficult — need to look up codes
- 5-year ACS has lag
- Не covers federal-level economics (use BLS/BEA для этого)

## Combine with

- **BLS** — для labor specifics
- **BEA** — для GDP
- **HUD** — для housing
