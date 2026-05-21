# Government & macro statistics

Источники для macro indicators, official government data, business sentiment, trade, tax. Cross-industry.

## United States

### FRED (Federal Reserve Economic Data)

**URL:** https://fred.stlouisfed.org/
**Type:** Government (Federal Reserve Bank of St. Louis)
**Access:** OPEN

**What's inside:**
- 800k+ economic time series
- GDP, inflation, employment, interest rates, monetary aggregates
- International data also (subset of OECD/IMF)
- Time series from many federal agencies aggregated

**When to use:**
- Любой macro claim про US economy (validation)
- Historical-data block за длинный период
- Forecast block (baseline from historical)
- Cross-country macro comparison (через FRED's international series)

**How to use:**
- Search: `fred.stlouisfed.org/series/<series-id>` (e.g., `GDPC1` для real GDP)
- Browse: `fred.stlouisfed.org/categories`
- Download CSV/JSON напрямую
- FRED API доступен (registration free)
- Search pattern: `site:fred.stlouisfed.org <indicator>`

**Data quality:**
- Credibility: A (federal reserve)
- Freshness: varies — daily/monthly/quarterly depending на series
- Lag: 1-60 days typical
- Methodology: linked для каждой series

**Limitations:**
- Mostly US-centric (international data is subset)
- No forecasts — only historical
- Some series revised over time (always check vintage)

**Combine with:**
- BLS (для labor detail)
- BEA (для GDP detail)
- World Bank (для global comparisons)

**Fallback if blocked:**
- BLS for labor data
- Treasury Direct для bond yields
- Macrotrends as data mirror

---

### BLS (Bureau of Labor Statistics)

**URL:** https://www.bls.gov/
**Type:** Government (US Department of Labor)
**Access:** OPEN

**What's inside:**
- Employment / unemployment
- CPI (consumer prices)
- PPI (producer prices)
- Productivity & costs
- Wages by industry/occupation/region
- Job openings (JOLTS)

**When to use:**
- Unit-economics block для labor cost
- Validation claims про US labor markets
- Wage data per occupation
- Historical inflation (CPI series)

**How to use:**
- Search: `bls.gov/<series>` (e.g., `bls.gov/cps` для current population survey)
- BLS Data Tool: `data.bls.gov`
- Search pattern: `site:bls.gov <topic>`
- API доступен (free with key)

**Data quality:**
- Credibility: A
- Freshness: monthly для most series
- Lag: 2-6 weeks

**Limitations:**
- US only
- Survey methodology — sample noise
- Definitions могут меняться year-over-year (CPI basket revisions)

**Combine with:**
- FRED (для time series)
- ADP National Employment Report (private payrolls cross-check)
- LinkedIn Workforce Reports (для qualitative)

---

### BEA (Bureau of Economic Analysis)

**URL:** https://www.bea.gov/
**Type:** Government (US Department of Commerce)
**Access:** OPEN

**What's inside:**
- GDP (national, regional, industry breakdown)
- Personal income and outlays
- International trade and investment
- Industry economic accounts

**When to use:**
- Market sizing US economy by sector
- Industry-level GDP contribution
- International trade balance claims

**How to use:**
- Interactive tables: `bea.gov/itable`
- Industry data: `bea.gov/industry`
- Search pattern: `site:bea.gov <topic>`

**Data quality:**
- Credibility: A
- Freshness: quarterly для GDP (advance/2nd/3rd estimates)
- Lag: 1 month для advance GDP estimate

**Limitations:**
- US only
- Revisions can be substantial

---

### US Census Bureau

**URL:** https://www.census.gov/
**Type:** Government
**Access:** OPEN

**What's inside:**
- Demographics (population, age, race, household composition)
- Economic census (every 5 years, deep industry data)
- Business formation statistics
- Trade in goods data (`census.gov/foreign-trade`)
- American Community Survey (ACS)

**When to use:**
- Demographic context (persona block)
- Business formation trends
- US trade statistics by country/product
- Market sizing by US geographic area

**How to use:**
- Data.census.gov
- Search pattern: `site:census.gov <topic>`

**Data quality:**
- Credibility: A
- Freshness: ACS yearly, Decennial каждые 10 лет
- Lag: 6-18 months

**Combine with:**
- BEA для economic data
- BLS для labor

---

### SEC EDGAR (US public company filings)

**URL:** https://www.sec.gov/edgar/
**Type:** Government (Securities and Exchange Commission)
**Access:** OPEN

См. `core/companies_public.md` для детальной записи. Включён здесь как cross-reference: SEC filings содержат macro-relevant data (aggregate corporate earnings, etc).

---

## Europe / EU

### Eurostat

**URL:** https://ec.europa.eu/eurostat/
**Type:** Intergovernmental (European Commission)
**Access:** OPEN

**What's inside:**
- EU 27 + EEA macro
- GDP, inflation (HICP), employment
- Trade between EU members + with rest of world
- Industry production indices
- Government finance
- Demographics

**When to use:**
- Macro EU/Eurozone claims
- Cross-country EU comparisons
- EU-specific trade data
- HICP inflation (EU equivalent of CPI)

**How to use:**
- Database: `ec.europa.eu/eurostat/data/database`
- API: REST and SDMX
- Bulk download
- Search pattern: `site:ec.europa.eu/eurostat <topic>`

**Data quality:**
- Credibility: A
- Freshness: varies — monthly to annual
- Lag: 1-12 months
- Methodology: ESS standards, well documented

**Limitations:**
- EU + EEA only (UK separated post-Brexit, partial data)
- Country-level data varies in quality (some weaker)

**Combine with:**
- ECB (для monetary/financial)
- National stat agencies (Destatis Germany, INSEE France, ONS UK)

---

### ECB Statistical Data Warehouse

**URL:** https://sdw.ecb.europa.eu/
**Type:** Intergovernmental (European Central Bank)
**Access:** OPEN

**What's inside:**
- Monetary policy data
- Interest rates, money supply
- Banking statistics
- Securities issuance
- Exchange rates
- Balance of payments
- Financial markets data

**When to use:**
- EU monetary claims
- ECB policy analysis
- EU banking sector data

**How to use:**
- Data warehouse: `sdw.ecb.europa.eu`
- Search pattern: `site:sdw.ecb.europa.eu <topic>`

**Data quality:**
- Credibility: A
- Freshness: daily/monthly
- Lag: minimal для financial markets data

---

### Bundesbank, INSEE, ONS (national EU)

**National statistical offices:**
- **Germany (Destatis):** https://www.destatis.de/EN/ — OPEN
- **France (INSEE):** https://www.insee.fr/en — OPEN
- **UK (ONS):** https://www.ons.gov.uk/ — OPEN
- **Italy (ISTAT):** https://www.istat.it/en/ — OPEN
- **Spain (INE):** https://www.ine.es/en — OPEN

Каждый — A-grade credibility, deeper detail чем Eurostat для своей страны.

---

## Global / International

### OECD Stats

**URL:** https://stats.oecd.org/
**Type:** Intergovernmental (OECD)
**Access:** OPEN

**What's inside:**
- 38 developed economies
- Comparable macro, trade, education, health
- Tax statistics database
- Productivity / unit labor costs
- Business confidence indicators

**When to use:**
- Cross-country comparisons developed economies
- Tax burden by country
- Productivity benchmarks

**How to use:**
- Browse: `stats.oecd.org/Index.aspx`
- Bulk download
- API через `data-explorer.oecd.org`
- Search pattern: `site:stats.oecd.org <topic>`

**Data quality:**
- Credibility: A
- Freshness: varies
- Lag: 6-24 months

**Combine with:**
- IMF для global non-OECD
- World Bank для developing economies

---

### World Bank Data

**URL:** https://data.worldbank.org/
**Type:** Intergovernmental (World Bank Group)
**Access:** OPEN

**What's inside:**
- Global development indicators (1400+)
- 200+ countries
- Income groups, regional aggregates
- World Development Indicators (WDI)
- Doing Business (archived но historical)

**When to use:**
- Global comparisons including developing countries
- Cross-country development indicators
- Historical (back to 1960 для some series)

**How to use:**
- Search: `data.worldbank.org/indicator/<indicator-code>`
- API: REST, free
- Bulk download
- Search pattern: `site:data.worldbank.org <topic>`

**Data quality:**
- Credibility: A
- Freshness: annual для most
- Lag: 1-2 years

**Limitations:**
- Self-reported data from countries quality varies
- Some series interpolated
- Doing Business discontinued 2021 (still archived)

---

### IMF Data

**URL:** https://www.imf.org/external/datamapper/
**Type:** Intergovernmental
**Access:** OPEN

**What's inside:**
- World Economic Outlook database
- International Financial Statistics
- Balance of Payments
- Government Finance Statistics
- Real-time forecasts (twice yearly WEO)

**When to use:**
- Global macro forecasts
- Fiscal/monetary data international
- Balance of payments analysis

**How to use:**
- Data mapper: `imf.org/external/datamapper`
- Data portal: `data.imf.org`
- Search pattern: `site:imf.org/external <topic>`

**Data quality:**
- Credibility: A
- Forecasts: B (forecasting hard)
- Lag: 6 months для historical

---

### BIS (Bank for International Settlements)

**URL:** https://www.bis.org/statistics/
**Type:** Intergovernmental
**Access:** OPEN

**What's inside:**
- Cross-border banking statistics
- Foreign exchange turnover (triennial survey)
- OTC derivatives
- Credit to private non-financial sector
- Property prices residential

**When to use:**
- International banking flows
- Currency markets
- Cross-border capital movements

**How to use:**
- Statistics portal: `bis.org/statistics`
- Search pattern: `site:bis.org/statistics <topic>`

**Data quality:**
- Credibility: A
- Lag: varies, sometimes 2 quarters

---

### Our World in Data

**URL:** https://ourworldindata.org/
**Type:** Academic (Oxford-based)
**Access:** OPEN

**What's inside:**
- Curated visualizations of global development data
- COVID-19 data (one of best aggregators)
- Climate, energy, health, education
- Sources properly cited (use as gateway)

**When to use:**
- Quick reference for global comparative claims
- Visualizations for explainer block
- Use as **gateway** к first-party sources cited

**How to use:**
- Browse by topic
- Each chart links к raw source — go there for citation
- Search pattern: `site:ourworldindata.org <topic>`

**Data quality:**
- Credibility: B (curator, not original collector)
- BUT cites A-grade sources — follow links

**Limitations:**
- Not primary source — always verify через cited source
- Updates can lag original sources

---

## Sentiment / PMI / Business confidence

### S&P Global PMI

**URL:** https://www.pmi.spglobal.com/
**Type:** Vendor (S&P Global, formerly IHS Markit)
**Access:** OPEN snapshots (full reports paywalled)

**What's inside:**
- Monthly PMI for 40+ countries
- Manufacturing PMI, Services PMI, Composite PMI
- Sub-indices: new orders, employment, input prices

**When to use:**
- Real-time business cycle indicator
- Forward-looking economic claims
- Cross-country business sentiment

**How to use:**
- Monthly press release with key numbers (OPEN)
- Detailed report paywalled
- Search pattern: `S&P Global Manufacturing PMI <country> <month>`

**Data quality:**
- Credibility: A — well-validated leading indicator
- Freshness: monthly, very current
- Lag: 1-2 weeks after month end

---

### ISM Reports (US)

**URL:** https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/
**Type:** Industry Body (Institute for Supply Management)
**Access:** OPEN headline numbers, full report members-only

**What's inside:**
- ISM Manufacturing PMI (>50 = expansion, <50 = contraction)
- ISM Services PMI
- Sub-indices

**When to use:**
- US business cycle indicator
- Leading indicator manufacturing

**How to use:**
- Press release with headline number (free)
- Search pattern: `ISM Manufacturing PMI <month>`

**Data quality:**
- Credibility: A
- Freshness: monthly, ~1st business day of month

---

### Fed Beige Book

**URL:** https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm
**Type:** Government (Federal Reserve)
**Access:** OPEN

**What's inside:**
- Qualitative business conditions 8 times/year
- 12 Fed districts contribute
- Industry-specific anecdotes

**When to use:**
- Qualitative US business conditions
- Regional variation in US economy
- Leading indicator (qualitative)

**How to use:**
- Each release as PDF/web text
- Search pattern: `Fed Beige Book <year> <district> <topic>`

**Data quality:**
- Credibility: A (Fed)
- Freshness: 8/year
- Lag: ~2 weeks

---

### Conference Board indicators

**URL:** https://www.conference-board.org/topics/us-leading-indicators
**Type:** Industry Body
**Access:** OPEN summaries, full paywalled

**What's inside:**
- Leading Economic Index (US, EU)
- Consumer Confidence Index
- CEO Confidence Survey

**When to use:**
- Forward-looking US/EU economic claims
- Consumer sentiment context

**How to use:**
- Monthly press releases (free)
- Search pattern: `Conference Board <indicator> <date>`

---

## Trade / Import-Export

### WTO Trade Statistics

**URL:** https://www.wto.org/statistics/
**Type:** Intergovernmental
**Access:** OPEN

**What's inside:**
- Global trade by country, sector
- Annual review of world trade
- Trade in services
- Tariff data

**When to use:**
- International trade claims
- Country trade balance
- Sector trade dynamics

**How to use:**
- Stats portal: `wto.org/statistics`
- Search pattern: `site:wto.org <topic>`

**Data quality:**
- Credibility: A
- Lag: 6-12 months

---

### UN Comtrade

**URL:** https://comtradeplus.un.org/
**Type:** Intergovernmental
**Access:** OPEN (registration for bulk)

**What's inside:**
- Bilateral trade flows by country pair
- Product detail (HS codes 6-10 digits)
- Annual + monthly data

**When to use:**
- Specific product trade flows between countries
- Granular trade analysis

**How to use:**
- Web portal с queries
- API доступен

**Data quality:**
- Credibility: A
- Freshness: monthly
- Lag: 2-6 months

---

### Observatory of Economic Complexity (OEC)

**URL:** https://oec.world/
**Type:** Academic/Vendor
**Access:** OPEN

**What's inside:**
- Visualized trade data
- Economic complexity index
- Country/product profiles

**When to use:**
- Quick trade visualization
- Economic complexity analysis

**How to use:**
- Browse by country или product
- Search pattern: `oec.world/en/profile/<type>/<id>`

---

### US Census Foreign Trade

**URL:** https://www.census.gov/foreign-trade/
**Type:** Government
**Access:** OPEN

**What's inside:**
- US imports/exports detailed
- Monthly trade data
- By country, commodity

**When to use:**
- US trade specific claims

---

## Tax data

### OECD Tax Database

**URL:** https://www.oecd.org/tax/tax-policy/tax-database/
**Type:** Intergovernmental
**Access:** OPEN

**What's inside:**
- Corporate tax rates by country
- Personal income tax
- VAT/GST rates
- Effective rates (not just statutory)
- Tax administration data

**When to use:**
- Tax burden comparison
- International tax planning context
- Regulatory context для decision block

**How to use:**
- Browse: `oecd.org/tax/tax-policy/tax-database`
- Search pattern: `site:oecd.org/tax <topic>`

**Data quality:**
- Credibility: A
- Lag: 1-2 years

---

### Tax Foundation

**URL:** https://taxfoundation.org/data/
**Type:** Think tank (US, libertarian-leaning)
**Access:** OPEN

**What's inside:**
- US and global tax research
- State tax climate index
- International tax competitiveness index

**When to use:**
- US state tax comparisons
- Tax policy critique perspective

**How to use:**
- Browse research and data

**Data quality:**
- Credibility: B (think tank, declared lean)
- Bias: 3 (libertarian framing)

---

### Eurostat Taxation

**URL:** https://taxation-customs.ec.europa.eu/index_en
**Type:** Intergovernmental (EU)
**Access:** OPEN

**What's inside:**
- EU tax statistics
- VAT rates by country
- Annual Taxation Trends report

**When to use:**
- EU-specific tax claims

---

## Country-specific recommended

### Russia / Russia (Rosstat)

**URL:** https://rosstat.gov.ru/
**Type:** Government
**Access:** OPEN

**What's inside:**
- Russian official statistics
- Population, GDP, inflation, industry production

**Limitations:**
- Periodic political adjustments — cross-check с external sources
- Recent data может быть suppressed
- English version limited

---

### China NBS (National Bureau of Statistics)

**URL:** http://www.stats.gov.cn/english/
**Type:** Government
**Access:** OPEN partial

**What's inside:**
- China official statistics
- Annual statistical yearbook

**Limitations:**
- Quality of granular data debatable
- Cross-check с external estimates (PMI surveys, satellite night lights data)
- Some series stop publication unexpectedly

---

### Statistics Canada

**URL:** https://www.statcan.gc.ca/
**Type:** Government
**Access:** OPEN

Similar structure to BLS/BEA but for Canada. High quality.

---

### ONS (UK)

**URL:** https://www.ons.gov.uk/
**Type:** Government
**Access:** OPEN

UK statistical agency, A-grade.

---

## Heritage Index / Doing Business / Economic Freedom

### Heritage Foundation Economic Freedom Index

**URL:** https://www.heritage.org/index/
**Type:** Think tank
**Access:** OPEN

**What's inside:**
- Annual ranking 184 countries on economic freedom
- 12 dimensions (rule of law, government size, regulatory efficiency, market openness)

**When to use:**
- Country business environment comparison
- Regulatory burden claims

**Data quality:**
- Credibility: B
- Bias: 3 (libertarian framing)

---

### Transparency International CPI

**URL:** https://www.transparency.org/cpi
**Type:** NGO
**Access:** OPEN

**What's inside:**
- Annual Corruption Perceptions Index
- 180 countries

**When to use:**
- Country governance comparisons
- Bribery/corruption context

---

## Quick reference — какой источник для какого вопроса

| Вопрос | Источник первого выбора |
|---|---|
| US GDP в YYYY | FRED `GDPC1` |
| US labor market | BLS |
| EU inflation | Eurostat HICP |
| Global GDP comparison | World Bank или IMF |
| Forward-looking business sentiment US | ISM PMI + Conference Board |
| Forward-looking business sentiment EU | S&P Global EU PMI |
| Bilateral trade China-Germany | UN Comtrade |
| Corporate tax по странам | OECD Tax Database |
| US state taxes | Tax Foundation |
| Country corruption | Transparency International |
| Country business freedom | Heritage Index или World Bank Doing Business (archived) |
| China macro (verified) | China NBS + external cross-check (S&P PMI, IEA data, satellite) |

## Common combining patterns

**Macro validation US:** FRED + BLS + BEA + ISM PMI (triangulation)

**Macro EU:** Eurostat + ECB + national stat agency + S&P PMI

**Global comparison:** IMF + World Bank + OECD + национальные (для verification)

**Forward look:** PMI + Conference Board + Fed Beige Book (US) — three different methodologies

**Tax burden:** OECD Tax Database + Tax Foundation + национальные ministries
