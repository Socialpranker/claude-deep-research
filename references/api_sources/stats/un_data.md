# UN Data API (SDMX)

## Overview

- **Endpoint base:** `https://data.un.org/ws/rest/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** http://data.un.org/Host.aspx?Content=API
- **Coverage:** UN-system data — demographics, SDGs, trade, environment

## Query patterns

### List dataflows

```
GET /dataflow/UNSD
```

### Get data

```
GET /data/{dataflow}/{key}?format=jsondata
```

### SDG indicators

```
GET /data/DF_SDG_GLH/.{indicator}..A?format=jsondata
```

## Use cases

- Global development indicators
- SDG (Sustainable Development Goals) tracking
- UN-specific data

## Limitations

- SDMX format awkward
- Coverage overlaps с World Bank, OECD — use те для большинства cases

## Combine with

- **World Bank** — usually better UX
- **OECD** — for developed countries
- **WHO** — для health specifically

## Notes

- Use UN Data в случаях где World Bank/OECD не хватает
- Для most research — World Bank is the better starting point
