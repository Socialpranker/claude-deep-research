# Public companies — financial data

Источники для public companies: SEC filings, financial data, stock data, financial APIs.

## United States

### SEC EDGAR

**URL:** https://www.sec.gov/edgar/
**Type:** Government (Securities and Exchange Commission)
**Access:** OPEN

**What's inside:**
- All US public company filings (10-K annual, 10-Q quarterly, 8-K events, S-1 IPO, 14A proxies)
- Form 4 insider transactions
- Form 13F institutional holdings
- Comments and correspondence with SEC

**When to use:**
- Due diligence US public company
- Validation financial claims о US public co
- Insider transactions / 13F holdings analysis
- IPO research (S-1)
- Materially-important events (8-K)

**How to use:**
- Full text search: `efts.sec.gov/LATEST/search-index?q=<query>`
- Company search: `sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<ticker>`
- Search pattern: `site:sec.gov/Archives <company> 10-K`
- API: free, no key required

**Data quality:**
- Credibility: A (legal obligation, audited)
- Freshness: real-time (filings appear within hours of submission)
- Lag: depends on filer's schedule

**Limitations:**
- Long documents — need to navigate to specific sections
- 8-K events not always significant (boilerplate compliance)
- Foreign companies file 20-F instead (different format)

**Combine with:**
- Stock Analysis / Macrotrends для parsed/clean version того же data
- News articles о filing events

**Fallback if blocked:**
- Stock Analysis (`stockanalysis.com`) has filings linked clean
- Macrotrends parses historical financials

---

### Stock Analysis

**URL:** https://stockanalysis.com/
**Type:** Vendor
**Access:** OPEN

**What's inside:**
- Clean parsed US/global stock data
- Income statement, balance sheet, cash flow (parsed from filings)
- Historical financials 10+ years
- Per-share metrics

**When to use:**
- Quick clean access к financials когда EDGAR filings overwhelming
- Cross-check parsed numbers

**How to use:**
- URL pattern: `stockanalysis.com/stocks/<ticker>/financials/`
- For non-US: `stockanalysis.com/stocks/<ticker>/financials/` + country
- Search pattern: `stockanalysis.com <ticker>`

**Data quality:**
- Credibility: B (third-party parser, not source)
- Cross-check с SEC EDGAR для critical claims

**Combine with:**
- SEC EDGAR (primary source)
- Yahoo Finance

---

### Macrotrends

**URL:** https://www.macrotrends.net/
**Type:** Vendor
**Access:** OPEN

**What's inside:**
- 10-20+ year historical financials для US public
- Margins, ratios, multiples historical
- Stock price history
- Annual + quarterly views

**When to use:**
- Historical-data block (financial time series)
- Trend analysis financial metrics
- Long-term cycles

**How to use:**
- URL pattern: `macrotrends.net/stocks/charts/<ticker>/<company-name>/<metric>`
- Search pattern: `macrotrends <ticker> <metric>`

**Data quality:**
- Credibility: B
- Freshness: lagging by 1-2 quarters

---

### Yahoo Finance

**URL:** https://finance.yahoo.com/
**Type:** Vendor
**Access:** OPEN

**What's inside:**
- Stock quotes, charts
- Basic financials (income, balance, cash flow)
- Earnings dates, EPS estimates
- News aggregation
- Options chains

**When to use:**
- Quick stock data lookup
- Earnings calendar
- Real-time price reference

**How to use:**
- `finance.yahoo.com/quote/<ticker>`
- Sub-pages: `/financials`, `/balance-sheet`, `/cash-flow`, `/key-statistics`

**Data quality:**
- Credibility: C-B (aggregator, some errors known)
- Freshness: real-time price; financials with delay

**Limitations:**
- Known data errors (cross-check critical claims)
- Historical depth limited compared to Macrotrends

---

### Finviz

**URL:** https://finviz.com/
**Type:** Vendor
**Access:** OPEN

**What's inside:**
- Stock screener (US-focused)
- Sector/industry heatmaps
- Insider transactions
- News aggregator
- Maps visualization

**When to use:**
- Screening US stocks by criteria
- Sector overview / heatmap visualization

**How to use:**
- Screener: `finviz.com/screener.ashx`
- Quote: `finviz.com/quote.ashx?t=<ticker>`

**Data quality:**
- Credibility: B
- US bias

---

## Europe / UK

### UK Companies House

**URL:** https://find-and-update.company-information.service.gov.uk/
**Type:** Government
**Access:** OPEN

**What's inside:**
- All UK registered companies (public and private)
- Annual accounts
- Directors / officers
- Shareholders disclosures
- Confirmation statements

**When to use:**
- UK company due diligence
- UK private company financials (unique advantage — UK requires private filings)

**How to use:**
- Search by company name or number
- API доступен (free with key)
- Search pattern: `site:find-and-update.company-information.service.gov.uk <company>`

**Data quality:**
- Credibility: A
- Freshness: filings обычно annual

**Combine with:**
- LSE для listed companies
- News для context

---

### Bundesanzeiger (Germany)

**URL:** https://www.bundesanzeiger.de/
**Type:** Government
**Access:** OPEN

**What's inside:**
- German company filings (Jahresabschluss / annual accounts)
- Required for GmbH, AG, and large companies
- Public announcements

**When to use:**
- German company due diligence
- German financial data

**How to use:**
- Search by company name
- Note: German interface, some English

---

### EU Financial Reporting (ESMA)

**URL:** https://www.esma.europa.eu/data
**Type:** Intergovernmental
**Access:** OPEN

**What's inside:**
- EU securities markets data
- Issuer information
- Transparency disclosures

---

## Canada

### SEDAR+

**URL:** https://www.sedarplus.ca/
**Type:** Government
**Access:** OPEN

**What's inside:**
- All Canadian public company filings
- Annual reports, prospectuses, insider reports

**When to use:**
- Canadian public company due diligence

---

## Asia-Pacific

### ASX Announcements (Australia)

**URL:** https://www.asx.com.au/asx/statistics/announcements.do
**Type:** Exchange
**Access:** OPEN

**What's inside:**
- ASX-listed company announcements
- Continuous disclosure

**When to use:**
- Australian listed companies

---

### TSE (Tokyo Stock Exchange)

**URL:** https://www.jpx.co.jp/english/
**Type:** Exchange
**Access:** OPEN partial

**What's inside:**
- Japan listed companies
- Statistics, indices

**Limitations:**
- Japanese language primary, English subset

---

### HKEX (Hong Kong)

**URL:** https://www.hkexnews.hk/
**Type:** Exchange
**Access:** OPEN

**What's inside:**
- Hong Kong-listed company filings
- Many China-related companies

**When to use:**
- HK-listed companies
- China-related entities listed in HK (alternative to mainland disclosure)

---

### SGX (Singapore)

**URL:** https://www.sgx.com/regulation/disclosures
**Type:** Exchange
**Access:** OPEN

**What's inside:**
- Singapore-listed company filings
- Disclosures

---

## ETF and Index Data

### ETF.com

**URL:** https://www.etf.com/
**Type:** Vendor
**Access:** OPEN

**What's inside:**
- ETF database (US-listed)
- Holdings, expense ratios, performance
- ETF screener

**When to use:**
- ETF research, holdings analysis
- Sector exposure через ETFs

---

### MSCI Indexes

**URL:** https://www.msci.com/indexes
**Type:** Vendor
**Access:** PARTIAL (overview free, full data paywall)

**What's inside:**
- Global equity indexes (MSCI World, EM, etc)
- Factor indexes
- ESG indexes

---

## Aggregators / Pro tools (partial open)

### Simply Wall St

**URL:** https://simplywall.st/
**Type:** Vendor
**Access:** PARTIAL (basic analysis free)

**What's inside:**
- Company analysis "snowflake" visualization
- DCF valuations
- Fair value estimates

**Data quality:**
- Credibility: B (algorithmic, not always nuanced)

---

### Koyfin

**URL:** https://www.koyfin.com/
**Type:** Vendor
**Access:** PARTIAL (free tier limited)

**What's inside:**
- Bloomberg-like financial data
- Charts, comparisons
- Macro data integrated

---

### Tikr Terminal

**URL:** https://www.tikr.com/
**Type:** Vendor
**Access:** PARTIAL

**What's inside:**
- Financial models, estimates
- Capital IQ-like data

---

## Stock-specific data

### Earnings call transcripts

**Sources:**
- Seeking Alpha (`seekingalpha.com/symbol/<ticker>/earnings`) — PARTIAL
- The Motley Fool (`fool.com`) — OPEN articles citing
- Company IR website — OPEN

**Search pattern:** `<company> "earnings call transcript" <quarter>`

---

### Analyst estimates

**Sources:**
- Yahoo Finance estimates page (`finance.yahoo.com/quote/<ticker>/analysis`) — OPEN
- Zacks (`zacks.com/stock/quote/<ticker>`) — PARTIAL
- StreetInsider (`streetinsider.com`) — PARTIAL

**Limitations:**
- Estimates have known biases (sell-side over-optimism)

---

### Insider transactions

**Sources:**
- SEC EDGAR Form 4 filings
- OpenInsider (`openinsider.com`) — OPEN parsed view
- Finviz Insider Tab — OPEN

**When to use:**
- Validation signals about company health
- Sentiment of management

---

### Institutional holdings (13F)

**Sources:**
- SEC EDGAR (13F filings)
- WhaleWisdom (`whalewisdom.com`) — OPEN parsed
- HedgeFollow (`hedgefollow.com`) — OPEN

**When to use:**
- Track major institutional positions
- Identify activist investors

---

## M&A and deal data

### Crunchbase Acquisitions

**URL:** https://www.crunchbase.com/discover/acquisitions
**Type:** Vendor
**Access:** PARTIAL

**What's inside:**
- M&A deals
- Acquirer, target, deal size (partial)

---

### Refinitiv / Mergermarket / Capital IQ

**Access:** PAYWALL (these are pro tools)
**Workaround:** Search для press releases citing these — `"Mergermarket" <industry> M&A <year>`

---

### Reuters Deals

**URL:** https://www.reuters.com/markets/deals/
**Type:** News (Thomson Reuters)
**Access:** OPEN articles

**When to use:**
- Recent M&A coverage
- Deal background

---

## Quick reference

| Что ищем | Источник |
|---|---|
| US 10-K | SEC EDGAR |
| US public company parsed financials | Stock Analysis или Macrotrends |
| UK private company accounts | Companies House (unique — UK requires private filings) |
| German company accounts | Bundesanzeiger |
| Insider buying/selling | SEC EDGAR Form 4 или OpenInsider |
| 13F institutional holdings | SEC EDGAR или WhaleWisdom |
| ETF holdings | ETF.com |
| Earnings calls | Seeking Alpha (partial) или company IR |
| Real-time stock price | Yahoo Finance / Finviz |
| Historical financials 10+ years | Macrotrends |

## Combining patterns

**Due diligence US public company:**
SEC EDGAR (10-K, 10-Q, 8-K) + Stock Analysis (parsed) + Macrotrends (history) + Yahoo Finance (recent) + Seeking Alpha (transcripts)

**Due diligence UK private company:**
Companies House (annual accounts) + news search + LinkedIn (для headcount, hiring)

**M&A analysis:**
Reuters/Bloomberg articles + SEC 8-K (для US public acquirer) + Crunchbase (для deal context)

**Insider/Institutional signal:**
SEC EDGAR Form 4 + OpenInsider + WhaleWisdom для 13F
