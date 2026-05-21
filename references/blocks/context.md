# CONTEXT blocks — внешний контекст

Блоки про контекст вокруг темы: регуляторика, гео, культура, история, политика, технологический стек, экосистема.

---

## X1 — `regulatory`

**Когда:** Финтех, медтех, AI, crypto, любой regulated domain.

**Что внутри:** Регуляторный контекст: законы, compliance requirements, ограничения по юрисдикциям.

**Антипаттерн:** Регуляторика как list без impact — нужно показать как влияет на тему.

**Композиция:** Перед `decision` или `landscape` если регуляторика критична.

**Шаблон:**

```markdown
## Regulatory context

### Юрисдикции и applicable regulations

| Юрисдикция | Регулятор | Ключевые требования | Status | Source |
|---|---|---|---|---|
| US | <SEC / FDA / etc> | <requirements> | active | [s03] |
| EU | <ESMA / EBA / DPC> | GDPR, MiCA, ... | active | [s07] |
| UK | FCA | <requirements> | active | [s11] |
| Asia | varies by country | — | varies | [s14] |

### Recent / upcoming changes
- **<Regulation A>** (effective <date>): <what changes> [s05]
- **<Regulation B>** (proposed): <if passes, impact ...>
- **Sunset clauses:** <if any regulations expire>

### Compliance burden
- **Light touch:** <jurisdictions>
- **Medium:** <jurisdictions>
- **Heavy:** <jurisdictions, e.g. EU MiCA>

### Banned / restricted
- В <country> запрещено <activity>
- В <country> ограничено <constraint>

### Regulatory risk for the topic
- **High risk:** if <event>, whole industry affected
- **Watch list:** <pending regulations to monitor>
- **Wins from regulation:** moats для compliance-ready players

### Source disclaimer
- Не legal advice. Регуляторика меняется быстро.
- Last update: <date>
- Для actual compliance — consult counsel.
```

---

## X2 — `geo-context`

**Когда:** Глобальные рынки, миграция, юрисдикции, gocrossing-cultural темы.

**Что внутри:** Различия по странам / регионам.

**Антипаттерн:** Generalizing «in Asia X happens» — Asia ≠ uniform. Будь конкретен.

**Композиция:** Дополнение к `landscape` или `regulatory`. Перед `cultural-context` если идут вместе.

**Шаблон:**

```markdown
## Geographic context

### Regional differences

| Region / Country | Что отличается | Why |
|---|---|---|
| US | <unique pattern> | <historical/economic reason> |
| EU | <pattern> | <reason> |
| China | <pattern> | <reason> |
| Japan | <pattern> | <reason> |
| Brazil | <pattern> | <reason> |
| India | <pattern> | <reason> |

### Hot markets
- **Fastest growing:** <country/region> — why [s07]
- **Mature / saturating:** <country/region>
- **Emerging / unexplored:** <country/region>

### Cross-border considerations
- Data sovereignty: <where data must stay>
- Currency / payment friction: <issues>
- Localization needs: <language, formats, cultural>

### Source
- Multi-country comparison from [s05]
- Local context from [s11], [s14]
```

---

## X3 — `cultural-context`

**Когда:** Кросс-культурные темы. Где культура влияет существенно.

**Что внутри:** Культурные особенности с конкретными impact на тему.

**Антипаттерн:** Стереотипы вместо observable patterns. Бери data-backed observations.

**Композиция:** После `geo-context`. Дополняет географию.

**Шаблон:**

```markdown
## Cultural context

### Culturally relevant patterns

#### Pattern 1: <observable cultural trait>
**Where:** <region / culture>
**What:** <observable behavior>
**Source:** [s05] (ethnographic study / survey)
**Impact on topic:** <как это меняет тему>

#### Pattern 2: ...

### Cross-cultural differences in this topic

| Dimension | Culture A | Culture B | Culture C |
|---|---|---|---|
| <relevant dim 1> | <how A approaches> | <how B> | <how C> |
| <relevant dim 2> | ... | ... | ... |

### Common mistakes (cultural blind spots)
- Westerners assuming X about Eastern markets — actually Y
- Tech assumptions universal — actually vary by culture

### Source-rigorous notes
- Avoid generalizations без backing data
- Cited cultural patterns from [s07] (peer-reviewed) and [s14] (industry survey N=2000)
```

---

## X4 — `historical-context`

**Когда:** Historical analysis. Deep explainer. Где «как мы сюда попали» критично.

**Что внутри:** Что было до и почему важно для понимания сейчас.

**Антипаттерн:** История ради истории. Каждый исторический факт должен relate to current understanding.

**Композиция:** В начале объяснения. Перед `mental-model` или `stepwise`.

**Шаблон:**

```markdown
## Historical context

### Origins (<period>)
**What existed before:** <предшествующее состояние>
**Key actors / movements:** <who/what mattered>
**Source:** [s05]

### Inflection points

#### <Year/event 1>
**What happened:** ...
**Why it mattered:** <changed trajectory>
**Source:** [s07]

#### <Year/event 2>
...

#### <Year/event 3>
...

### Path dependency
Что мы имеем сейчас существует именно так потому что:
- Decision X in <year> locked in <pattern>
- Failed attempts at Y in <year> made people skeptical of <approach>
- Standard Z became default по historical accident

### Если бы история пошла иначе
- Counterfactual 1: если бы <event A> не произошло → <different world>
- Counterfactual 2: если бы <person B> не сделал <X> → <different now>

### Why historical context matters for current decisions
- Path dependency means <current option> easier than <theoretical better option>
- Cultural memory of <past failure> makes <X> politically hard
- Existing infrastructure investments lock in <pattern>
```

---

## X5 — `political-context`

**Когда:** Geopolitics, sanctions, market access, government-related темы.

**Что внутри:** Политические факторы влияющие на тему.

**Антипаттерн:** Partisan framing. Стараться нейтрально по форме, факт-based.

**Композиция:** Дополнение к `regulatory` или `geo-context`. Когда политика влияет существенно.

**Шаблон:**

```markdown
## Political context

### Government stance (by jurisdiction)
- **US:** <current admin position> — может измениться после next election
- **EU:** <position> — driven by <commission body>
- **China:** <position> — strategic priority for <reason>
- **Russia:** <if relevant>
- **Other:** <country-specific positions>

### Geopolitical tensions affecting topic
- **Tension 1:** <description>, affects via <mechanism>
- **Tension 2:** <description>

### Sanctions / trade restrictions
- <country X> blocked from <activity Y>
- <country Z> faces tariffs on <category>
- Source: [s07]

### Political risk
- **High risk:** <if scenario X happens>
- **Watch list:** <upcoming elections, policy changes>
- **Stable factors:** <bipartisan consensus areas>

### Influence groups / lobbies
- <Group A> lobbying for <position>
- <Group B> opposing
- Outcome leans toward <if known>

### What could change
- Election in <country/year>
- <new admin position>
- International agreement <pending>

### Sources & neutrality
- Multiple sources from different perspectives: [s03] (left-leaning), [s07] (right-leaning), [s11] (centrist)
- Aim for triangulation, не единственная точка зрения
```

---

## X6 — `tech-stack-context`

**Когда:** Tech research. Когда нужно понимать какие технологии в основе.

**Что внутри:** Технологии в основе темы + dependencies + alternatives.

**Антипаттерн:** Tech listing без понимания "what for". Каждая tech должна объяснять role.

**Композиция:** В технических explainer. Перед `mental-model` для tech-heavy тем.

**Шаблон:**

```markdown
## Tech stack context

### Foundational technologies
- **<Tech A>** — что: <role in topic>, why это используется
- **<Tech B>** — что: <role>, alternatives: <list>
- **<Tech C>** — что: <role>, history: was once <alternative> until <event>

### Architecture pattern (high-level)
```
[Layer 1: ...] — implemented with <Tech A>
[Layer 2: ...] — implemented with <Tech B>
[Layer 3: ...] — implemented with <Tech C>
```

### Dependencies
- Topic depends on <external tech/service X>
- If X breaks / changes, topic affected
- Backup / alternatives: <if any>

### Common variants of the stack
- **Variant 1:** Tech A + Tech B + alternative для C
- **Variant 2:** Different combination — when preferred
- **Variant 3:** Minimal — for prototyping

### Tech maturity
- **Mature / stable:** <techs that won't change>
- **Active development:** <techs in flux>
- **Experimental:** <bleeding edge>

### Lock-in risks
- <Tech X> creates vendor lock-in via <mechanism>
- Migration complexity: <high / medium / low>

### Source
- [s03] (technical deep-dive)
- [s07] (architectural blog from practitioners)
```

---

## X7 — `ecosystem`

**Когда:** Platform analysis. Когда тема — часть большей экосистемы.

**Что внутри:** Соседи, дополняющие, конкурирующие платформы вокруг темы.

**Антипаттерн:** Перечисление всех связанных вещей. Только релевантные ecosystem players.

**Композиция:** После `landscape` или дополняет его. Расширяет границы за пределы прямых конкурентов.

**Шаблон:**

```markdown
## Ecosystem

### Subject в центре экосистемы

```
              ┌─── Customers / Users ───┐
              ▼                         ▼
       ┌──── SUBJECT ────┐
       │                 │
       │                 │
       ▼                 ▼
[Suppliers/Inputs]   [Complementors]
       │                 │
       └─── Competitors ─┘
       └─── Substitutes ─┘
```

### Stakeholder groups

#### Customers / Users
- <segment 1> — needs: ..., budget: ...
- <segment 2> — needs: ...

#### Suppliers / Inputs
- <supplier A> — provides: <what>
- <supplier B> — provides: <what>

#### Complementors (make subject more valuable)
- <complementor X> — increases value of subject by <mechanism>
- <complementor Y> — без них subject less useful

#### Substitutes (alternative ways to achieve same goal)
- <substitute A> — when chosen over subject
- <substitute B> — emerging substitute

#### Direct competitors
- See `landscape` / `profile-card`

### Strategic implications
- **Strong complementors:** <which strengthen our subject>
- **Weak suppliers:** <bottleneck on which subject depends>
- **Emerging substitutes:** <potential disruption>

### Ecosystem health
- Net new entrants per year: <N>
- M&A activity: <high/low>
- Investor interest: <signals>
- Maturity: emerging / growing / mature / declining

### Source
- Industry overview from [s05]
- Ecosystem mapping from [s11]
```
