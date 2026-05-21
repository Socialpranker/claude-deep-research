# Science — citation databases, replication, retractions

Для academic search vies см. `channels.md` (channel `academic`, `preprint-servers`, `conference-proceedings`). Здесь — metadata sources, citation databases, retraction tracking.

## Citation databases

### Google Scholar
**URL:** scholar.google.com
**Access:** OPEN
**What:** Broad scholarly search across 100M+ papers
**When:** general academic search starting point
**Quality:** B (aggregator, citation counts may be inflated)
**Limitations:** algorithm opaque; some predatory journals indexed

### Semantic Scholar
**URL:** semanticscholar.org
**Access:** OPEN
**What:** AI-powered academic search — 200M+ papers + semantic features
**When:** finding related papers, citation context
**Quality:** B-A; API доступен (free)

### OpenAlex
**URL:** openalex.org
**Access:** OPEN
**What:** Open scholarly knowledge graph (replaces Microsoft Academic Graph)
**When:** large-scale scholarly metadata analysis
**Quality:** A
**API:** free, REST

### CrossRef
**URL:** crossref.org
**Access:** OPEN
**What:** DOI registration agency — metadata for 130M+ scholarly works
**When:** DOI lookup, citation resolution
**API:** free

### ORCID
**URL:** orcid.org
**Access:** OPEN
**What:** Researcher identification + affiliations
**When:** disambiguate researcher names

### DOAJ (Directory of Open Access Journals)
**URL:** doaj.org
**Access:** OPEN
**What:** ~20k vetted open access journals
**When:** finding legitimate OA journals (avoid predatory)

### Scopus / Web of Science
**Access:** PAYWALL (institutional subscription)
**What:** Traditional citation databases
**Fallback:** Use Google Scholar + Semantic Scholar + OpenAlex для most uses

## Retraction tracking

### Retraction Watch
**URL:** retractionwatch.com
**Access:** OPEN (blog + database)
**What:** Database of retracted scientific papers (50k+ entries)
**When:** validation — check if paper retracted!
**Quality:** A — careful journalism
**Critical:** ALWAYS check before citing important paper

### PubPeer
**URL:** pubpeer.com
**Access:** OPEN
**What:** Post-publication peer review — comments on papers (including misconduct detection)
**When:** finding criticisms of specific papers
**Quality:** B (comments quality varies but often substantive)

## Replication / Methodology

### COS (Center for Open Science)
**URL:** cos.io
**Access:** OPEN
**What:** Open science research — Reproducibility Projects
**When:** replication status of fields

### Replication Database
**URL:** replicationindex.com
**Access:** OPEN
**What:** Replication attempts tracker
**When:** validation научных claims через replication

### Many Labs Projects
Search для "Many Labs <field>" — collaborative replication projects:
- Many Labs (psychology — Klein et al.)
- Many Labs 2, 3, 4...
- Many Babies, Many Smiles, etc

## Scientific output / output metrics

### Nature Index
**URL:** natureindex.com
**Access:** OPEN
**What:** Tracking institutional/country output in 82 top journals
**When:** research strength comparison (with caveat — top journals only)

### SCImago Journal Rank
**URL:** scimagojr.com
**Access:** OPEN
**What:** Journal rankings, h-index
**When:** journal quality assessment

### Altmetric
**URL:** altmetric.com
**Access:** PARTIAL (free for individual papers через bookmarklet)
**What:** Alternative metrics — social media, news attention to papers
**When:** societal impact of research (not just citations)

## Pre-registration / Open data

### OSF (Open Science Framework)
**URL:** osf.io
**Access:** OPEN
**What:** Pre-registrations, open data, materials
**When:** check if study pre-registered (boost confidence)

### AsPredicted
**URL:** aspredicted.org
**Access:** OPEN
**What:** Pre-registration platform
**When:** confirming pre-registration

## Research integrity / fraud detection

### Forensic tools
- **Imagetwin / Proofig** — image manipulation detection — services
- **GPTZero / similar AI detectors** — для checking AI-generated content
- **iThenticate** — plagiarism (institutional access)

### Whistleblower / fraud cases
- **Retraction Watch** (already listed) — primary source
- **Science integrity in news** — search `<paper> fraud OR misconduct`

## Quick reference

| Что ищем | Источник |
|---|---|
| Search academic literature broadly | Google Scholar + Semantic Scholar |
| Open knowledge graph | OpenAlex |
| DOI lookup | CrossRef |
| Researcher disambiguation | ORCID |
| Retraction check | Retraction Watch (ALWAYS check) |
| Paper criticism / post-pub review | PubPeer |
| Replication status of field | COS + Many Labs project results |
| Journal ranking | SCImago JR + Nature Index |
| Alternative metrics (social attention) | Altmetric |
| Pre-registration check | OSF + AsPredicted |

## Critical reminders

- **ALWAYS check Retraction Watch** before citing key papers. Retracted papers can stay cited for years.
- **Citation count ≠ correctness.** Highly cited can be wrong (e.g., Mason-Dixon meta-analyses with fraud).
- **Pre-registration** boosts credibility — check OSF.
- **Replication crisis varies by field:** worst in psychology, some medicine. Better in physics, math.
- **Predatory journals** exist on Google Scholar — verify via DOAJ + journal reputation.

## Combining patterns

**Validating научного claim:**
PubMed/Scholar (find studies) → Retraction Watch check → Cochrane systematic review (if exists) → replication status (COS/Many Labs/related) → PubPeer comments → methodology critique (см. validate.md V9)

**Finding all papers by researcher:**
Google Scholar + Semantic Scholar + ORCID page + institutional faculty page + ArXiv author page

**Citation network analysis:**
OpenAlex (machine-readable) + Semantic Scholar (semantic relations) + CrossRef (DOI graph)
