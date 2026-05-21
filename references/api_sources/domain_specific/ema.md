# European Medicines Agency (EMA)

## Overview

- **API:** EMA не имеет официального REST API — данные через скрейпинг + downloadable datasets
- **Bulk data:** https://www.ema.europa.eu/en/medicines/download-medicine-data
- **Coverage:** Все EU-approved drugs + safety updates

## What's available

Без REST API но есть:

1. **EPAR (European Public Assessment Reports)** — PDF per drug
2. **Medicine database** — searchable web interface
3. **Downloadable CSV** — periodically updated

## Workflow

Для агента: используй WebFetch на EMA pages.

### Find drug

```
WebFetch: https://www.ema.europa.eu/en/medicines/human/EPAR/{drug-name}
```

### Search

```
WebFetch: https://www.ema.europa.eu/en/medicines?search_api_views_fulltext={query}
```

## Use cases

- EU regulatory status drug
- EPAR scientific assessment
- Safety updates / pharmacovigilance

## Combine with

- **FDA Drugs@FDA** — для US equivalent
- **ClinicalTrials.gov** — для trial context
- **PubMed** — для literature

## Notes

- EMA — slower data publication than FDA
- Critical для understanding EU drug approval ≠ FDA approval
