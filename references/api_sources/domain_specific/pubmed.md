# PubMed E-utilities

## Overview

- **Endpoint base:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Auth:** None (optional key для higher rate)
- **Free tier:** 3 req/sec без key, 10 req/sec с key
- **Docs:** https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Coverage:** 36M+ biomedical citations + abstracts

## Auth setup (optional)

1. https://www.ncbi.nlm.nih.gov/account/ → register
2. Settings → API Key Management → create
3. `export NCBI_API_KEY="..."`

## Query patterns

### Search PubMed

```
GET /esearch.fcgi?db=pubmed&term={query}&retmax=50&retmode=json&api_key={key}
# Returns list of PMIDs
```

### Get article summaries

```
GET /esummary.fcgi?db=pubmed&id={pmid1},{pmid2}&retmode=json&api_key={key}
```

### Get full records (abstracts)

```
GET /efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text&api_key={key}
```

### Linked articles (citations + similar)

```
GET /elink.fcgi?dbfrom=pubmed&db=pubmed&id={pmid}&linkname=pubmed_pubmed_citedin
```

## Example queries

**Phase 4 — medical literature scan:**

```
GET /esearch.fcgi?db=pubmed&term=intermittent+fasting+metabolic+health&retmax=50&sort=date&retmode=json
```

**Phase 4 — meta-analyses:**

```
GET /esearch.fcgi?db=pubmed&term=intermittent+fasting+AND+meta-analysis%5BPublication+Type%5D&retmax=20&retmode=json
```

## Useful filters

- `[Publication Type]` — Meta-Analysis, Review, Clinical Trial, RCT
- `[MeSH Terms]` — Medical Subject Headings
- `AND`, `OR`, `NOT`
- `2020:2024[Date - Publication]`

## Combine with

- **ClinicalTrials.gov** — trials specifically
- **Cochrane Library** — systematic reviews
- **Semantic Scholar** — для broader scholarly context
- **OpenAlex** — для citation graph

## Notes

- PubMed — definitive medical literature index
- E-utilities API стабильно работают decades
- Free, no key required для most uses
