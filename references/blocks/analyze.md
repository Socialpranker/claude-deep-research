# ANALYZE blocks — структурированный анализ

Блоки для структурированных аналитических разрезов: tables, SWOT, root cause, etc.

---

## A1 — `data-table`

**Когда:** Custom для «по показателям» вопросов. Любая сравнительная аналитика с заранее определёнными метриками.

**Что внутри:** Параметрическая таблица объект × показатель.

**Антипаттерн:** Включать показатели «потому что есть данные». Только те что отвечают на вопрос пользователя.

**Композиция:** Базовый блок для custom-сравнения. Часто комбинируется с `profile-card`.

**Шаблон:**

```markdown
## <Объекты> по показателям

| Объект | Показатель 1 | Показатель 2 | Показатель 3 | Показатель 4 | Источник |
|---|---|---|---|---|---|
| Item A | <value> | <value> | <value> | <value> | [s03] |
| Item B | <value> | <value> | <value> | <value> | [s05] |
| Item C | <value> | <value> | <value> | <value> | [s07] |
| Item D | <value> | <value> | <value> | <value> | [s11] |

### Definitions показателей
- **Показатель 1:** <как измеряется, в каких единицах>
- **Показатель 2:** ...
- **Показатель 3:** ...

### Quality of data
- For Item A: данные за <дату>, источник [s03] — Credibility 5
- Для Item B: estimates только (точных публичных нет) — Credibility 3
- Для Items C, D: comparable, current

### Observations
- <Item X> лидирует по <показатель>
- <Item Y> явный outlier по <показатель> — почему
- Разброс по <показатель>: <min>-<max>, median <Z>
```

---

## A2 — `timeline`

**Когда:** Custom для исторических / sequential тем.

**Что внутри:** Хронология с датами и значимостью каждого события.

**Антипаттерн:** Хронология без significance — кажется trivia. Каждое событие должно объяснять «и что».

**Композиция:** Альтернатива `stepwise` для исторических тем. Дополнение к `historical-context`.

**Шаблон:**

```markdown
## Timeline

### YYYY-MM-DD — <Событие 1>
**Что произошло:** ...
**Significance:** <почему это поворотный момент>
**Источник:** [s03]

### YYYY-MM-DD — <Событие 2>
**Что произошло:** ...
**Significance:** ...
**Источник:** [s07]

### YYYY-MM-DD — <Событие 3>
...

### Patterns в timeline
- **Acceleration:** события идут чаще после <date>
- **Catalysts:** <event X> запустил <chain of events Y, Z>
- **Inflection point:** <date> — после неё всё стало по-другому

### Ключевые игроки / authors во времени
- Person A: active 2015-2020, заложил основы
- Person B: continued 2018-current, развивает в направлении X
- ...
```

---

## A3 — `qa-list`

**Когда:** Q&A-жанр всегда. Custom как дополнение к другим жанрам.

**Что внутри:** Атомарные Q→A с confidence и source links.

**Антипаттерн:** Вопросы не атомарные («Q1: расскажи всё про X»). Один вопрос = один ответ.

**Композиция:** Главный блок Q&A. В других жанрах — дополнительная секция.

**Шаблон:**

```markdown
## Q&A

### Q1: <конкретный вопрос своими словами>
**Ответ:** <2-4 предложения>
**Confidence:** high | medium | low — <если ниже high, почему>
**Откуда:** [s03](sources/03_*.md), [s12](sources/12_*.md), [s17](sources/17_*.md)
**Нюансы:** <оговорки, контекст применимости>

### Q2: <вопрос>
**Ответ:** ...
**Confidence:** ...
**Откуда:** ...
**Нюансы:** ...

### Q3: ...
### Q4: ...
### Q5: ...
```

---

## A4 — `hypotheses-outcome`

**Когда:** Q&A, validation, любой ресёрч с явными hypotheses в plan.md.

**Что внутри:** Таблица: гипотеза → статус → источники.

**Антипаттерн:** Молча отказаться от гипотезы из plan. Каждая должна получить status.

**Композиция:** Перед `closing` секцией. Замыкает loop с plan.md.

**Шаблон:**

```markdown
## Hypotheses outcome

| Гипотеза | Статус | Источники | Комментарий |
|---|---|---|---|
| H1: <тезис> | ✅ confirmed | s01, s07, s12 | Подтверждена 3 разнотипными |
| H2: <тезис> | ⚠️ partial | s03, s15 | Только при условии X |
| H3: <тезис> | ❌ contradicted | s09, s11, s14 | Опровергнута 3 источниками |
| H4: <тезис> | 🤷 insufficient | — | Данных недостаточно, см. Open Questions |

### Что говорит результат
- 2 из 4 гипотез подтверждены — ожидаемый результат
- H3 contradicted — это neat finding, фиксируем
- H4 — нужен другой подход / next research
```

---

## A5 — `swot`

**Когда:** Business/product/strategic analysis. Classic SWOT.

**Что внутри:** 4 квадранта: Strengths, Weaknesses (внутренние), Opportunities, Threats (внешние).

**Антипаттерн:** Перепутать внутреннее и внешнее. S и W — про сам объект, O и T — про среду.

**Композиция:** Дополнение к decision или landscape. Перед `recommendation`.

**Шаблон:**

```markdown
## SWOT

### Strengths (internal, positive)
- ✅ ... [s03]
- ✅ ...

### Weaknesses (internal, negative)
- ❌ ... [s07]
- ❌ ...

### Opportunities (external, positive)
- 💡 ... [s11]
- 💡 ...

### Threats (external, negative)
- ⚠️ ... [s15]
- ⚠️ ...

### Reading the SWOT
- **S × O (best):** how strengths can capture opportunities → <strategy>
- **W × T (worst):** what weaknesses make us vulnerable to threats → <mitigation>
- **S × T:** use strengths to defend against threats
- **W × O:** address weaknesses to access opportunities
```

---

## A6 — `risk-register`

**Когда:** Custom для рискованных решений. Project planning, business decisions.

**Что внутри:** Реестр рисков с probability × impact + mitigation.

**Антипаттерн:** Без mitigation — реестр становится списком тревог.

**Композиция:** В decision для рискованных. После `options-matrix`.

**Шаблон:**

```markdown
## Risk register

| ID | Risk | Probability | Impact | Risk score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R1 | <risk description> | high | high | 9 | <action> | <who> |
| R2 | <risk> | medium | high | 6 | <action> | <who> |
| R3 | <risk> | high | low | 3 | accept | — |
| R4 | <risk> | low | high | 3 | watch + plan | <who> |
| R5 | <risk> | low | low | 1 | ignore | — |

**Scoring:** probability (1-3) × impact (1-3). Risks ≥6 — top priority.

### Top risks (>=6)
- **R1:** <expanded explanation, why it's the biggest>
- **R2:** ...

### Risk acceptance
- Какой уровень риска допустим — <threshold>
- Кто принимает риск — <person/role>
- Что триггерит escalation — <signal>
```

---

## A7 — `dependency-graph`

**Когда:** Project planning. System analysis. Что от чего зависит.

**Что внутри:** Узлы + dependencies + critical path.

**Антипаттерн:** Дерево без направления. Зависимости направлены — A зависит от B.

**Композиция:** Custom для проектных ресёрчей. Альтернатива `flow-diagram` для статичных систем.

**Шаблон:**

```markdown
## Dependencies

```
                ┌──── E ◄─── A
                │
       D ◄────── B ◄─── C
       │
       └──► F ──► G
```

**Reading:** A depends on E. B depends on E and is required by D. C → B → D chain.

### Critical path
- A → E → B → D — longest path
- Latency этой цепи: <если время — Z hours/days/weeks>

### Dependency types
- **Hard:** A не работает без B (strong dependency)
- **Soft:** A работает хуже без B (degraded)
- **Optional:** A может работать без B

### Risks от dependencies
- Если падает E — упадут A, B, D (high blast radius)
- Если падает F — только G (low blast radius)
- Single points of failure: <узлы>
```

---

## A8 — `bottleneck-analysis`

**Когда:** Performance analysis. Ops. Любой анализ узких мест.

**Что внутри:** Где узкое место + почему + как идентифицировать.

**Антипаттерн:** «Где-то медленно» без конкретики. Bottleneck — конкретный component с конкретным limit.

**Композиция:** В технических explainer или validation perf claims. После `flow-diagram` если есть.

**Шаблон:**

```markdown
## Bottleneck analysis

### Current bottleneck: <component>
**Limit:** <конкретный, e.g. CPU 95%, latency 200ms, throughput 1k req/s>
**Why:** <root cause — например, single-threaded, network-bound, etc>
**Signals:** <как видим в metrics>
**Impact:** <что чувствует пользователь>

### Downstream impact
- <Component A>: forced to wait
- <Component B>: drops requests

### If this bottleneck removed — next bottleneck would be
- **<Component X>** — limit: <Z>
- Then: **<Component Y>**

**Order of optimization:**
1. Fix current (<expected improvement>)
2. Then watch for next
3. Don't optimize early — current is dominant

### Why it became a bottleneck
- <historical reason>
- <design decision>
- <load growth>
```

---

## A9 — `force-field`

**Когда:** Change analysis. Lewin's force field — какие силы за и против изменения.

**Что внутри:** Силы FOR change vs силы AGAINST. Magnitudes.

**Антипаттерн:** Не оценивать magnitude — все силы кажутся равными. Реально нет.

**Композиция:** Custom для organizational/strategic анализа. Альтернатива SWOT.

**Шаблон:**

```markdown
## Force field analysis

**Proposed change:** <что меняем>

### Forces FOR change (driving)
| Force | Magnitude | Description | Source |
|---|---|---|---|
| F1 | high | <description> | [s03] |
| F2 | medium | ... | [s07] |
| F3 | low | ... | — |

### Forces AGAINST change (restraining)
| Force | Magnitude | Description | Source |
|---|---|---|---|
| R1 | high | <description> | [s05] |
| R2 | medium | ... | [s11] |
| R3 | low | ... | — |

### Net force
- Forces FOR (high): N
- Forces AGAINST (high): M
- **Net direction:** <change happens / change blocked / equilibrium>

### Strategy
- **To enable change:** weaken which restraining force?
- **Strongest leverage:** R1 has high magnitude — find way to address
- **Easiest leverage:** R3 is low — pick low-hanging fruit
```

---

## A10 — `5-whys`

**Когда:** Root cause analysis. Любой «почему X происходит» вопрос.

**Что внутри:** Цепочка «почему» 5 уровней до root cause.

**Антипаттерн:** Останавливаться на первом «потому что». Идти до root.

**Композиция:** Custom для debugging/diagnostic ресёрчей. Дополнение к `dependency-graph`.

**Шаблон:**

```markdown
## 5 Whys

**Problem:** <observable issue>

**Why 1:** <первая причина>
**Source for this answer:** [s03]

**Why 2 (why does that happen):** <вторая причина>
**Source:** [s07]

**Why 3:** ...

**Why 4:** ...

**Why 5 (root cause):** <fundamental cause>
**Source:** [s11]

### Root cause
<суммарно — что является fundamental cause>

### Fix at which level?
- Fixing at Level 1 — quick fix, problem returns
- Fixing at Level 3 — partial solution
- **Fixing at Level 5 (root) — permanent solution but expensive**

### Caveats
- 5-whys works for sequential cause chains, не для complex systems
- В сложных системах может быть несколько root causes
- Возможно нужно дополнить причинной диаграммой Ishikawa
```

---

## A11 — `swot-extended`

**Когда:** Strategic analysis. Когда хочешь не просто SWOT, а actionable.

**Что внутри:** SWOT + actionable из каждого квадранта (TOWS matrix).

**Антипаттерн:** Использовать вместо basic SWOT когда хватает basic.

**Композиция:** Усиленная версия `swot`. Не использовать вместе.

**Шаблон:**

```markdown
## Extended SWOT (with actions)

### Strengths
- S1: ... [s03]
- S2: ...

### Weaknesses
- W1: ... [s05]
- W2: ...

### Opportunities
- O1: ... [s07]
- O2: ...

### Threats
- T1: ... [s11]
- T2: ...

### TOWS matrix — actionable strategies

|     | **Opportunities** | **Threats** |
|---|---|---|
| **Strengths** | **SO strategies (use S to capture O):**<br>1. S1 + O1 → <action><br>2. S2 + O2 → <action> | **ST strategies (use S to defend from T):**<br>1. S1 vs T1 → <action> |
| **Weaknesses** | **WO strategies (fix W to access O):**<br>1. Fix W1 → enables O1 | **WT strategies (minimize W exposure to T):**<br>1. <action> |

### Priority of actions
1. <highest priority action with rationale>
2. ...
```

---

## A12 — `pestle`

**Когда:** Macro analysis. Market environment analysis.

**Что внутри:** Political/Economic/Social/Technological/Legal/Environmental factors.

**Антипаттерн:** Заполнять каждую категорию обязательно. Если в Environmental ничего relevant — пропусти.

**Композиция:** Custom для broad market/industry analysis. Может предшествовать landscape.

**Шаблон:**

```markdown
## PESTLE analysis

### Political
- <factor> — impact: high/medium/low — direction: ↑ favorable / ↓ adverse / ↔ neutral [s03]
- ...

### Economic
- <factor> — impact, direction
- Inflation, currency, interest rates if relevant

### Social
- <demographic/cultural shift>
- Consumer behavior changes

### Technological
- <emerging tech disruption>
- Platform shifts

### Legal
- <regulatory changes>
- <new compliance requirements>

### Environmental
- <if relevant — climate, sustainability>
- Если нет relevance: write "n/a, не релевантно теме"

### Summary
- **Net environment:** favorable / hostile / mixed
- **Dominant factors:** <top 2-3 across all categories>
- **Watch list:** factors which could shift quickly
```

---

## A13 — `before-after`

**Когда:** Impact analysis. До и после изменения.

**Что внутри:** Метрики до и после с дельтой.

**Антипаттерн:** Только after numbers без before. Нет контекста.

**Композиция:** Custom для validation эффекта changes.

**Шаблон:**

```markdown
## Before / After

**Change:** <что произошло>
**Date:** <когда>
**Population:** <who/what affected>

### Metrics

| Metric | Before | After | Δ (abs) | Δ (%) | Significance |
|---|---|---|---|---|---|
| <metric 1> | 100 | 150 | +50 | +50% | high (statistically sig) |
| <metric 2> | 5 | 4.8 | -0.2 | -4% | not significant |
| <metric 3> | $1000 | $800 | -$200 | -20% | high |

### Attribution
- Уверенность что изменение вызвано change: high | medium | low
- Confounders:
  - Other changes одновременно <тоже изменилось>
  - Seasonality
  - Selection bias

### Counterfactual
- Что бы случилось без change: <baseline projection> [s07]
- Difference vs counterfactual: <numbers>

### Lessons
- <takeaway 1>
- <takeaway 2>
```
