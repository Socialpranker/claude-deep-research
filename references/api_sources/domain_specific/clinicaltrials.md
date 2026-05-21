# ClinicalTrials.gov API v2

## Overview

- **Endpoint base:** `https://clinicaltrials.gov/api/v2/`
- **Auth:** None
- **Free tier:** Unlimited
- **Docs:** https://clinicaltrials.gov/data-api/api
- **Coverage:** 400k+ clinical trials globally (required for FDA-regulated)

## Query patterns

### Search studies

```
GET /studies?query.term={condition}&pageSize=20
```

### Filter by status

```
GET /studies?query.term={condition}&filter.overallStatus=RECRUITING,ACTIVE_NOT_RECRUITING&pageSize=20
```

### Specific NCT ID

```
GET /studies/{NCTId}
```

### By sponsor

```
GET /studies?query.locn=&filter.lead=Pfizer&pageSize=50
```

## Example queries

**Phase 4 — find ongoing trials:**

```
GET /studies?query.cond=diabetes&filter.overallStatus=RECRUITING&pageSize=50
```

**Phase 4 — meta-data for analysis:**

```
GET /studies?query.cond=COVID-19&filter.phase=PHASE3&fields=NCTId,BriefTitle,LeadSponsorName,OverallStatus
```

## Useful fields

- `NCTId` — unique identifier
- `BriefTitle`, `OfficialTitle`
- `OverallStatus` — Recruiting / Completed / Terminated
- `Phase` — PHASE1 / PHASE2 / PHASE3 / PHASE4
- `EnrollmentCount`
- `StudyType`
- `LeadSponsorName`
- `Conditions`, `Interventions`

## Use cases

- Drug development pipeline analysis
- Find recruitment status
- Sponsor research (pharma company portfolios)
- Validate study design / sample size

## Limitations

- Trials Not all registered (small academic studies sometimes missed)
- Results not always uploaded (reporting compliance issue)

## Combine with

- **PubMed** — published results
- **FDA Drugs@FDA** — approval decisions
- **EMA** — for EU equivalent
