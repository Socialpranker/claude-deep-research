# OECD SDMX API

## Overview

- **Endpoint base:** `https://sdmx.oecd.org/public/rest/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** https://data-explorer.oecd.org/
- **Coverage:** Developed countries — labor, trade, education, health, environment

## What it returns

SDMX-JSON (Statistical Data and Metadata Exchange standard) — complex но structured.

## Query patterns

```
GET /data/{dataflow}/{key}/all?startTime=2020&endTime=2024&dimensionAtObservation=AllDimensions&format=json
```

Examples:
- Unemployment: `GET /data/DSD_LFS@DF_IALFS_UNE_M/...`
- GDP: `GET /data/DSD_NAAG@DF_NAAG/...`

## Use cases

- Cross-country developed comparisons
- OECD-specific indicators (PISA, PIAAC scores)
- More frequent updates than World Bank

## Combine with

- **World Bank** — для developing countries
- **FRED** — для US детали
- **Eurostat** — для EU specific

## Notes

SDMX format hardcore. Если не нужны bulk queries — проще brouse https://data.oecd.org/ и WebFetch конкретные tables.
