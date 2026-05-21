# PEOPLE blocks — люди, команды, поведение

Блоки про человеческое измерение темы: personas, organizations, individuals, behaviors, incentives.

---

## P1 — `persona`

**Когда:** UX research, product analysis, customer-centric ресёрчи.

**Что внутри:** Профили пользователей с needs, behaviors, pain points.

**Антипаттерн:** Демографические profiles без needs ("33 years old female") — не работают для design decisions. Бери jobs-to-be-done framing.

**Композиция:** Перед `user-journey` если есть. Custom для UX-ресёрчей.

**Шаблон:**

```markdown
## Personas

### Persona 1: <name/role>
**Кто:** <короткое описание — роль, контекст>
**Goals:** что хочет достичь
**Pain points:**
- <pain 1> — [s03]
- <pain 2>
**Current behaviors:**
- Что делает сейчас для своих goals
**Tools they use:** <existing solutions>
**Decision criteria:** <как выбирают tools>
**Source basis:** <interviews / surveys / app reviews — [s05]>

### Persona 2: <name/role>
...

### Anti-persona (кому НЕ подходит)
**Кто это:** ...
**Почему не подходит:** ...
```

---

## P2 — `team-org`

**Когда:** Конкурент-анализ, due diligence, organizational research.

**Что внутри:** Структура команды/организации, ключевые роли, отношения.

**Антипаттерн:** Просто список людей без понимания их роли в принятии решений.

**Композиция:** Дополнение к `profile-card` для глубокого due diligence.

**Шаблон:**

```markdown
## Team / Org structure

### <Company X>

**Total headcount:** N (as of <date>)

**Org structure:**
```
          ┌──────── CEO ────────┐
          │                     │
    ┌─────▼─────┐         ┌─────▼─────┐
    │  CTO      │         │   COO     │
    └─────┬─────┘         └───────────┘
          │
    ┌─────┴────────┬────────────┐
    ▼              ▼            ▼
  Eng (N)     ML (N)       Product (N)
```

**Key functional groups:**
- **Engineering** — N people, lead: <name>
- **ML** — N people, lead: <name>
- **Product** — N people, lead: <name>
- **GTM** — N people, lead: <name>

**Signals from structure:**
- ML team растёт быстро → ML-driven roadmap
- No dedicated security → security as side responsibility
- Sales/CS ratio: <N/M> → product-led vs sales-led

**Hiring activity (last 6 months):**
- N new hires in <function>
- Specific roles: <list>
- Что это значит: <expansion in X area>

**Source:** [s07] (LinkedIn analysis), [s11] (job postings)
```

---

## P3 — `key-people`

**Когда:** Понимание ключевых людей в индустрии. Кто за чем стоит.

**Что внутри:** Карточки людей: bio, прошлые проекты, влияние.

**Антипаттерн:** Слишком много людей — список без приоритизации. Бери ключевых (5-10), не всех.

**Композиция:** Дополнение к `profile-card` или `landscape`. Глубокий due diligence.

**Шаблон:**

```markdown
## Key people

### <Person 1 Name> — <current role>

**Bio:** <короткая био>
**Prior:** <prev companies/projects>
**Education:** <если relevant>
**Achievements:** <что reach значимое>
**Influence:** <насколько влияет на область — 1-5>
**Public presence:** Twitter @, blog, recent talks
**Conflict of interest considerations:** <если ангажирован к determined view>
**Source:** [s05]

### <Person 2 Name> — <role>
...

### Networks of key people
- <Person 1> и <Person 2> часто collab — same alma mater
- <Person 3> воспринимается как opponent к мнению <Person 1>
- <Person 4> — emerging voice, недавно появился

### Where these people speak / publish
- <conferences>
- <publications>
- <podcasts>
```

---

## P4 — `user-journey`

**Когда:** UX, product design. Когда нужно понять путь пользователя.

**Что внутри:** Steps + что user делает + что чувствует + где friction.

**Антипаттерн:** Только actions без emotions — friction не выявить.

**Композиция:** После `persona`. Часто комбинируется.

**Шаблон:**

```markdown
## User journey: <persona> achieving <goal>

### Step 1: <Awareness / Discovery>
**Trigger:** что заставило начать
**Action:** <что user делает>
**Touchpoints:** <где взаимодействует — web/app/email>
**Emotion:** 😊 / 😐 / 😟 / 😡
**Friction:** <если есть — что мешает>
**Source:** [s03]

### Step 2: <Consideration>
...

### Step 3: <Decision>
...

### Step 4: <Purchase / Sign-up / Commit>
...

### Step 5: <Onboarding>
...

### Step 6: <Active use>
...

### Step 7: <Retention / Churn>
...

### Pain points summary
- 🔴 Step 3 — биггест friction: <description> [s07]
- 🟡 Step 5 — onboarding too long
- 🟢 Step 6 — works smoothly

### Time investment
- Time to first value: <X minutes/hours>
- Total time to commit: <X days/weeks>
```

---

## P5 — `behavioral-patterns`

**Когда:** Behavioral analysis. Trading behavior, user behavior, market behavior.

**Что внутри:** Паттерны поведения участников + их сила + триггеры.

**Антипаттерн:** Описание поведения без objective signal (как мы знаем что это паттерн).

**Композиция:** Custom для behavioral/economic ресёрчей. После `persona` если есть.

**Шаблон:**

```markdown
## Behavioral patterns

### Pattern 1: <название>
**Что делают:** <описание поведения>
**Когда:** <триггер / условия>
**Кто:** <какие участники>
**Sample:** N=<observed>
**Strength:** consistent | occasional | rare
**Direction:** rational | irrational | strategic
**Source:** [s07]

**Why this happens (hypotheses):**
- Incentive structure (см. `incentive-structure`)
- Cognitive bias: <bias name>
- Information asymmetry
- Coordination dynamics

**Implications for X:** <что это значит для нашей темы>

### Pattern 2: <название>
...

### Pattern 3: <название>
...

### Anti-patterns (что DOESN'T happen вопреки ожиданиям)
- Никто не делает <expected behavior> — почему: ...
```

---

## P6 — `incentive-structure`

**Когда:** Game theory, market design, organizational analysis.

**Что внутри:** Кто что получает, какие стимулы у каждого участника.

**Антипаттерн:** Игнорировать misaligned incentives. Часто конфликт интересов = ключ объяснения.

**Композиция:** До `behavioral-patterns`. Объясняет «почему так».

**Шаблон:**

```markdown
## Incentive structure

### Участники

| Actor | Получает | Платит | Net incentive | Strength |
|---|---|---|---|---|
| A | <gain> | <cost> | <direction> | high |
| B | <gain> | <cost> | <direction> | medium |
| C | <gain> | <cost> | <direction> | low |

### Detailed analysis

#### Actor A
- **Primary motive:** <что главное для A>
- **What A optimizes:** <конкретная метрика>
- **Constraints:** <что не может делать>
- **Conflict with whom:** <A vs B>
- **Source:** [s05]

#### Actor B
...

### Misalignments (где интересы расходятся)
- A vs B: A maximizes X, B maximizes ¬X
- Result: <observable conflict>

### Aligned incentives (где сходятся)
- A and C both want Y
- Result: <observable cooperation>

### Equilibrium (если есть)
- В текущей системе stable state: <description>
- Causal model: <как одни поведения стабилизируют другие>

### How to shift behavior
- Изменить incentive: <if X changed, then A would do Y>
- Mechanism design: <leverage point>
```

---

## P7 — `expert-opinion`

**Когда:** Expert-driven validation. Когда мнение экспертов критично.

**Что внутри:** Карточка эксперта с opinion и conflict of interest.

**Антипаттерн:** Принимать мнение эксперта без оценки conflicts. Эксперты тоже biased.

**Композиция:** В validation как specific evidence type. Альтернатива `evidence-graded` для qualitative claims.

**Шаблон:**

```markdown
## Expert opinions

### Expert 1: <Name> — <credentials>

**Stated opinion:** <что говорит, dirvect quote или close>
**Source:** [s05] (interview / talk / paper)
**Date:** <when said>

**Credentials:**
- N years in <field>
- Published in <journals>
- Position at <institution>

**Independence:**
- **Funded by:** <source — может быть conflict>
- **Affiliations:** <relevant ones>
- **Past stances:** <consistent / changed view recently>
- **Conflict of interest:** <yes/no/possible>

**Trust score:** A (independent + credentialed) | B (credentialed but conflicted) | C (anecdotal)

### Expert 2: <Name>
...

### Aggregate of expert opinions
- Consensus: <если есть>
- Disagreement: <where>
- Independent vs conflicted ratio: <N/M>

### Caveats
- Все эксперты в одной школе мысли → возможен groupthink
- Эксперты разных школ → see `conflicting-evidence`
```
