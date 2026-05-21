# NUMBERS blocks — количественные данные

Блоки для quantitative claims: metrics, market sizing, forecasts, benchmarks.

---

## N1 — `metric-tracker`

**Когда:** «По метрикам», «по KPI», любой ресёрч с конкретными числовыми показателями.

**Что внутри:** Метрики с цифрами, единицами, временем, источниками.

**Антипаттерн:** Цифры без единиц или времени — бесполезны. Каждое число с context.

**Композиция:** Custom для quantitative ресёрчей. Часто комбинируется с `data-table` или `profile-card`.

**Шаблон:**

```markdown
## Metrics

| Metric | Value | Unit | As of | Confidence | Source |
|---|---|---|---|---|---|
| <metric 1> | 1,200 | active users | 2025-Q4 | high | [s03] |
| <metric 2> | $4.5M | ARR | 2025-12 | medium (estimate) | [s07] |
| <metric 3> | 18% | YoY growth | 2024→2025 | high | [s05] |
| <metric 4> | 95ms | P95 latency | benchmark | high | [s11] |
| <metric 5> | 0.4% | conversion rate | 30-day avg | medium | [s14] |

### Metric definitions
- **<metric 1>:** how it's measured, what counts as "active"
- **<metric 2>:** ARR formula used
- **<metric 3>:** methodology of YoY calculation

### Metric quality notes
- <metric 2> is an estimate from public signals, не official
- <metric 5> varies seasonally — value is average

### Movement / trends
- <metric 1> grew from N to M over period
- <metric 5> declining: <hypothesis why>
```

---

## N2 — `market-sizing`

**Когда:** Market research. Когда нужно понять размер рынка.

**Что внутри:** TAM/SAM/SOM или другая sizing методология.

**Антипаттерн:** Слишком оптимистичный TAM без обоснования. Каждый layer должен иметь top-down и bottom-up validation.

**Композиция:** Custom для market analysis. Перед `landscape` для контекста.

**Шаблон:**

```markdown
## Market sizing

### TAM (Total Addressable Market)
**Value:** ~$<X>B
**Definition:** все потенциальные покупатели вне зависимости от reach
**Methodology:** top-down (industry reports) ИЛИ bottom-up (users × ARPU)
**Top-down estimate:** [s03] — $X.YB
**Bottom-up estimate:** <calc> — $X.YB
**Convergence:** <если оба подхода сходятся, confidence higher>
**Confidence:** medium

### SAM (Serviceable Addressable Market)
**Value:** ~$<X>B (X% от TAM)
**Definition:** TAM minus segments которые мы не можем reach (geography, regulations, etc)
**Excluded:** <segment 1>, <segment 2>
**Confidence:** medium

### SOM (Serviceable Obtainable Market)
**Value:** ~$<X>M (X% от SAM)
**Definition:** реалистично достижимый рынок за <timeframe>
**Reasoning:** <obstacles, competitive constraints>
**Confidence:** low (depends on execution)

### Growth projections
- TAM growing at <X>% YoY [s05]
- SAM expanding via <regulatory change / new tech>
- SOM reachable in <X years>

### Caveats
- "Markets" overlap with adjacent — clean delineation hard
- Top-down reports часто inflate by N% (industry interest)
- Bottom-up rely on multiple assumptions
```

---

## N3 — `growth-rates`

**Когда:** Growth analysis. YoY / CAGR / MoM.

**Что внутри:** Темпы роста с диапазонами и источниками.

**Антипаттерн:** Один rate без context (short period? cherry-picked?). Покажи временное окно.

**Композиция:** Дополнение к `metric-tracker` или `trends`.

**Шаблон:**

```markdown
## Growth rates

### YoY (year-over-year)
| Metric | 2022 | 2023 | 2024 | 2025 | YoY 2024→2025 | Source |
|---|---|---|---|---|---|---|
| Users | 100k | 200k | 350k | 500k | +43% | [s03] |
| Revenue | $1M | $2M | $4M | $7M | +75% | [s07] |
| Margin | 30% | 32% | 35% | 36% | +3pp | [s11] |

### CAGR (compound annual growth rate)
- Users 2022→2025: CAGR = <X%>
- Revenue 2022→2025: CAGR = <Y%>

### Comparison to peers
- Industry avg CAGR (users): <X%>
- Industry avg CAGR (revenue): <Y%>
- This company vs industry: <faster / slower / on par>

### Sustainability
- Is this growth sustainable? <factors>
- Decay signals: <if seen>
- Growth quality: revenue per user growing or flat?
```

---

## N4 — `unit-economics`

**Когда:** SaaS / business analysis. CAC, LTV, payback period.

**Что внутри:** Unit economics formula с numbers.

**Антипаттерн:** Только LTV/CAC ratio без abstraction over time. LTV растёт со временем, CAC падает — снапшот вводит в заблуждение.

**Композиция:** Custom для product/business analysis. Дополнение к `metric-tracker`.

**Шаблон:**

```markdown
## Unit economics

### Customer Acquisition
- **CAC:** $<X>
- **CAC components:**
  - Marketing spend / new customer: $<X>
  - Sales cost / new customer: $<Y>
  - Total CAC: $<Z>
- **CAC payback period:** <N months>
- **Source:** [s07]

### Customer Value
- **Average revenue per user (ARPU):** $<X>/month
- **Average customer lifespan:** <X months>
- **Gross LTV:** $<X> (ARPU × lifespan)
- **Net LTV (with churn-adjusted):** $<X>
- **LTV / CAC ratio:** <X> (healthy: >3, unhealthy: <1)

### Margin
- **Gross margin:** <X>%
- **Net margin:** <Y>%
- **Contribution margin per unit:** $<Z>

### Cohort behavior
- 30-day retention: <X>%
- 90-day retention: <X>%
- 12-month retention: <X>%
- Annual revenue retention: <X>% (negative if expansion > churn)

### Health indicators
- ✅/❌ LTV/CAC > 3
- ✅/❌ CAC payback < 12 months
- ✅/❌ Gross margin > 70% (for SaaS)
- ✅/❌ Net revenue retention > 100%
```

---

## N5 — `cost-breakdown`

**Когда:** Финансовый анализ. Due diligence. Понимание structures of costs.

**Что внутри:** Структура затрат с долями.

**Антипаттерн:** Общие категории без drill-down. Если "infrastructure" — что именно?

**Композиция:** Custom для financial. Дополнение к `unit-economics`.

**Шаблон:**

```markdown
## Cost breakdown

### Total monthly costs: $<X>

| Category | $/month | % | Notes |
|---|---|---|---|
| Infrastructure | $X | Y% | Cloud + 3rd party APIs |
| Salaries (Eng) | $X | Y% | N FTE × avg $Z |
| Salaries (other) | $X | Y% | Sales, ops, finance |
| Marketing | $X | Y% | Mostly paid acq |
| Office / overhead | $X | Y% | — |
| Software / tools | $X | Y% | — |
| **Total** | **$X** | **100%** | |

### Variable vs fixed
- **Variable** (scales with usage): <X>% — infrastructure, API costs
- **Fixed** (constant): <Y>% — salaries, office, software

### Per-unit cost
- Cost / active user: $<X>
- Cost / transaction: $<Y>
- Cost / new customer (CAC component): $<Z>

### Cost trends
- Last 12 months trend: <category X grew Y%>
- Outlier: <category that's surprising>

### Optimization opportunities
- <category 1>: could reduce <X%> by <action>
- <category 2>: locked in for <reason>

### Source
- [s05] — public filings / leaked deck / estimates
```

---

## N6 — `benchmark-numbers`

**Когда:** Performance analysis. Когда нужны industry benchmarks для сравнения.

**Что внутри:** Industry-wide benchmarks для метрик.

**Антипаттерн:** Старые benchmarks (>2 years). Cherry-picked benchmarks без range.

**Композиция:** Дополнение к `metric-tracker` для context.

**Шаблон:**

```markdown
## Industry benchmarks

| Metric | Industry P25 | P50 | P75 | P90 | Best-in-class | Source |
|---|---|---|---|---|---|---|
| Gross margin | 50% | 65% | 75% | 80% | 85%+ | [s07] |
| LTV/CAC | 1.5 | 3.0 | 4.5 | 6.0 | 8.0+ | [s11] |
| Annual churn | 15% | 8% | 4% | 2% | <1% | [s03] |
| Time to PMF | 24mo | 18mo | 12mo | 9mo | <6mo | [s14] |

### Methodology behind benchmarks
- Sample: <type of companies — SaaS B2B, ARR $1-10M, etc>
- N: <how many companies in benchmark>
- Year: <when collected>
- Caveat: <bias of survey responders>

### Where THIS subject sits
- Metric 1: P40 (below median)
- Metric 2: P70 (above median)
- Metric 3: P85 (top quartile)

### Implications
- Metric 1 below median → top priority for improvement
- Metric 3 already best-in-class → don't over-invest, maintain
```

---

## N7 — `forecast`

**Когда:** Прогнозирование. Любое утверждение о будущих значениях.

**Что внутри:** Прогнозы с диапазонами и допущениями.

**Антипаттерн:** Точечный forecast без интервала ("will be $5M next year"). Forecast always range.

**Композиция:** Custom для prediction-heavy ресёрчей. После `growth-rates` или `historical-data`.

**Шаблон:**

```markdown
## Forecast

**Metric:** <what we forecast>
**Horizon:** <e.g. 12 months / 3 years>
**Forecast date:** <YYYY-MM-DD>

### Scenarios

| Scenario | Probability | Value at horizon | Assumptions |
|---|---|---|---|
| Pessimistic | 25% | <X> | <key downside assumptions> |
| Realistic | 50% | <Y> | <baseline assumptions> |
| Optimistic | 25% | <Z> | <key upside assumptions> |

### Methodology
- **Base:** historical CAGR of X% [s07]
- **Adjustments:**
  - Market saturation effect: -Y%
  - New product launches: +Z%
  - Competitive pressure: -W%
- **Final base rate:** <result>

### Key assumptions
- A1: <market continues at current pace>
- A2: <no major regulatory change>
- A3: <key personnel stays>

### Sensitivity analysis
- If A1 fails: <new forecast range>
- If A2 fails (regulation): <new forecast>
- Most fragile assumption: <which>

### Validity / track record
- Past forecasts by same method: hit rate <X%>
- Confidence interval: <how wide>

### When to update forecast
- After Q1 results (recalibrate baseline)
- If <major event> happens
- See `update-triggers`
```

---

## N8 — `historical-data`

**Когда:** Data analysis, trend research. Когда нужен временной ряд.

**Что внутри:** Историческая time series с данными и аномалиями.

**Антипаттерн:** Только final values без full series. Конкретные точки во времени могут показать сюжет.

**Композиция:** Перед `forecast` или `trends`. Дополнение к `metric-tracker`.

**Шаблон:**

```markdown
## Historical data

**Metric:** <what we track>
**Period:** <YYYY-MM to YYYY-MM>
**Frequency:** annual / quarterly / monthly / daily

### Time series

| Period | Value | Notable events | Source |
|---|---|---|---|
| 2020-Q1 | <X> | COVID start | [s03] |
| 2020-Q2 | <Y> | lockdowns | [s03] |
| 2020-Q3 | <X> | reopening | [s05] |
| 2020-Q4 | <X> | — | [s05] |
| 2021-Q1 | <X> | new product launch | [s07] |
| ... | ... | ... | ... |
| 2025-Q4 | <X> | current | [s11] |

### Visualization (ASCII sparkline if simple)

```
Value
  ▲
8 │                              ●
6 │                          ● ● 
4 │                ● ● ● ●
2 │      ● ●  ●  ●
  └─────────────────────────────► time
   '20  '21  '22  '23  '24  '25
```

### Notable events / inflections
- 2020-Q2: drop -X% (COVID effect)
- 2021-Q3: jump +Y% (new product launch)
- 2023-Q1: plateau начался — почему: [s07]
- 2024-Q4: recovery — [s11]

### Patterns
- Seasonality: <yes/no, какая>
- Cyclicality: <yes/no>
- Trend: <linear / exponential / decay / cyclic>

### Outliers
- 2022-Q3: anomaly — <explanation>
- 2024-Q1: anomaly — <explanation>

### Quality of historical data
- Pre-2020: estimates from secondary sources
- 2020-2022: company-reported, audited
- 2023+: primary public filings
```
