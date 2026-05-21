# Health / Medical / Public health

Medical data, public health, clinical trials. Для pharma industry-specific смотри `industries/pharma.md`.

## Public health agencies

### CDC (Centers for Disease Control)
**URL:** cdc.gov/data-statistics
**Access:** OPEN
**What:** US public health — disease surveillance, vaccination, mortality, BRFSS surveys
**When:** US health claims, disease trends, public health policy
**Quality:** A
**Key sub-portals:**
- CDC Wonder (`wonder.cdc.gov`) — mortality data
- NHIS (National Health Interview Survey) — survey data
- BRFSS — behavioral risk factor surveillance

### WHO (World Health Organization)
**URL:** who.int/data
**Access:** OPEN
**What:** Global health statistics, disease burden, health indicators
**When:** global health claims, cross-country comparison
**Quality:** A
**Key resources:**
- Global Health Observatory (`who.int/data/gho`)
- Global Burden of Disease through IHME

### IHME / Global Burden of Disease
**URL:** vizhub.healthdata.org/gbd-results
**Access:** OPEN
**What:** Comprehensive disease burden by country, DALYs, mortality causes
**When:** disease burden claims, public health prioritization
**Quality:** A — peer-reviewed methodology

### Our World in Data — Health
**URL:** ourworldindata.org/health
**Access:** OPEN
**What:** Curated visualizations of global health data (uses WHO/IHME)
**When:** quick gateway к primary sources

### KFF (Kaiser Family Foundation)
**URL:** kff.org/research-data
**Access:** OPEN
**What:** US health policy data, especially insurance/Medicare/Medicaid
**When:** US health policy research

### OECD Health Statistics
**URL:** oecd.org/health/health-statistics
**Access:** OPEN
**What:** OECD member countries health data — spending, outcomes, workforce
**When:** developed-country health system comparison

## Clinical trials

### ClinicalTrials.gov
**URL:** clinicaltrials.gov
**Access:** OPEN
**What:** US + global clinical trial registry
**When:** finding trials for specific condition/intervention, validation научных claims о trials
**Quality:** A — required by law to register
**Search pattern:** `clinicaltrials.gov/search?cond=<condition>&intr=<intervention>`

### EU Clinical Trials Register
**URL:** clinicaltrialsregister.eu
**Access:** OPEN
**What:** EU registered trials
**When:** EU trial research

### WHO ICTRP
**URL:** trialsearch.who.int
**Access:** OPEN
**What:** International registry meta-search (incl. EU, US, others)
**When:** comprehensive trial search

## Drug & medical device approvals

### FDA Drugs@FDA
**URL:** accessdata.fda.gov/scripts/cder
**Access:** OPEN
**What:** US drug approvals, prescribing information, applications
**When:** US drug approval research

### EMA (European Medicines)
**URL:** ema.europa.eu
**Access:** OPEN
**What:** EU drug approvals, scientific opinions
**When:** EU drug regulatory research

### FDA Adverse Event Reporting (FAERS)
**URL:** fda.gov/drugs/questions-and-answers-fdas-adverse-event-reporting-system-faers
**Access:** OPEN
**What:** Reported adverse events for drugs
**When:** drug safety analysis

### Drug Information Portal
**URL:** druginfo.nlm.nih.gov
**Access:** OPEN
**What:** NIH-curated drug information
**When:** drug fact lookup

## Medical literature

### PubMed
**URL:** ncbi.nlm.nih.gov/pubmed
**Access:** OPEN
**What:** 36M+ biomedical literature citations + abstracts
**When:** medical literature search
**Quality:** A — peer-reviewed
**See also:** academic channel в channels.md

### Cochrane Reviews
**URL:** cochranelibrary.com
**Access:** PARTIAL (abstracts free, full reviews paywall)
**What:** Systematic reviews — gold standard for evidence
**When:** validation medical claims via highest-quality evidence
**Quality:** A — meta-analyses
**Fallback:** Author preprints, PubMed-indexed summaries

### TRIP Database
**URL:** tripdatabase.com
**Access:** PARTIAL
**What:** Clinical search engine for evidence-based medicine
**When:** clinical decision support, EBM research

## Health economics / Insurance

### KFF (continued)
US health insurance, policy economics

### MEPS (Medical Expenditure Panel Survey)
**URL:** meps.ahrq.gov
**Access:** OPEN
**What:** US health expenditures
**When:** US health spending research

## Nutrition / Food

### USDA FoodData Central
**URL:** fdc.nal.usda.gov
**Access:** OPEN
**What:** Food composition database
**When:** nutrition research, food data

### Global Dietary Database
**URL:** globaldietarydatabase.org
**Access:** OPEN
**What:** Global dietary intake data
**When:** global nutrition research

## Survey-based health data

### NHANES (US)
**URL:** cdc.gov/nchs/nhanes
**Access:** OPEN
**What:** National Health and Nutrition Examination Survey
**When:** US population health metrics — measured (not self-reported)

### NHIS (US)
**URL:** cdc.gov/nchs/nhis
**Access:** OPEN
**What:** National Health Interview Survey (self-reported)
**When:** US self-reported health behaviors

### Eurobarometer (EU)
**URL:** ec.europa.eu/eurobarometer
**Access:** OPEN
**What:** EU public opinion surveys including health attitudes
**When:** EU health attitudes/awareness

## Pandemic-specific (legacy but useful)

### COVID-19 data sources
- **JHU CSSE Dashboard** (archived) — github.com/CSSEGISandData/COVID-19
- **OWID COVID** — `ourworldindata.org/coronavirus`
- **WHO COVID-19** — `who.int/emergencies/diseases/novel-coronavirus-2019`

## Quick reference

| Что ищем | Источник |
|---|---|
| US disease surveillance | CDC |
| Global disease burden | WHO + IHME GBD |
| US drug approval | FDA Drugs@FDA |
| EU drug approval | EMA |
| Clinical trial для condition | ClinicalTrials.gov |
| Medical literature | PubMed (см. academic channel) |
| Best evidence (meta-analysis) | Cochrane Library |
| US health spending | MEPS + KFF |
| Cross-country health system | OECD Health Statistics |
| Adverse drug events | FAERS |
| Food composition | USDA FoodData |
| Measured US population health | NHANES (measured) vs NHIS (self-report) |

## Critical reminders

- **Self-reported vs measured.** NHIS = self-reported, NHANES = measured — большая разница в quality.
- **Cochrane > single RCT > observational.** Иерархия evidence.
- **Industry-funded studies** — possible bias; check funding disclosure.
- **Country differences** — health systems и definitions varies, careful с comparisons.

## Combining patterns

**Disease burden claim:** WHO + IHME GBD + OWID (visualization) + CDC (US specific) + Cochrane (interventional evidence)

**Drug effectiveness validation:**
PubMed (find studies) + Cochrane (systematic review) + ClinicalTrials.gov (full trial picture incl. unpublished) + FDA approval doc + FAERS (safety signal)

**Health system comparison:**
OECD Health Statistics + KFF (US) + national stat agencies + WHO comparable data
