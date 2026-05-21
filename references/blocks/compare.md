# COMPARE blocks — сравнение и выбор

Блоки для decision-жанра и любых ресёрчей где нужно сравнить опции.

---

## C1 — `options-matrix`

**Когда:** Decision. Сравнение опций по критериям без весов.

**Что внутри:** Таблица опции × критерии. Числовая оценка 1-5 или качественная.

**Антипаттерн:** Все критерии равнозначны — реально один-два решают. Если критерии неравнозначны — бери `weighted-score`.

**Композиция:** После `decision-context`. До `weighted-score` если хочешь оба (matrix + scoring).

**Шаблон:**

```markdown
## Options matrix

| Критерий | Option A | Option B | Option C |
|---|---|---|---|
| Latency | 5 | 3 | 4 |
| Cost | 3 | 5 | 4 |
| Dev velocity | 4 | 5 | 3 |
| Reliability | 5 | 4 | 4 |
| Vendor lock-in (less is better) | 4 | 2 | 5 |
| **Sum** | **21** | **19** | **20** |

**Score legend:** 5=Best-in-class, 4=Strong, 3=Average, 2=Below average, 1=Weak/Missing.

**Что не вошло в матрицу (потому что одинаково):** ...
```

---

## C2 — `weighted-score`

**Когда:** Decision когда критерии имеют разный вес.

**Что внутри:** Опции × критерии × веса → weighted total.

**Антипаттерн:** Прятать веса в footnotes. Веса должны быть прозрачны и обсуждаемы.

**Композиция:** После `decision-context`. Альтернатива или дополнение к `options-matrix`.

**Шаблон:**

```markdown
## Weighted score

Веса по приоритетам из decision-context:

| Критерий | Вес | A score | A weighted | B score | B weighted | C score | C weighted |
|---|---|---|---|---|---|---|---|
| Latency | 3 | 5 | 15 | 3 | 9 | 4 | 12 |
| Cost | 2 | 3 | 6 | 5 | 10 | 4 | 8 |
| Dev velocity | 2 | 4 | 8 | 5 | 10 | 3 | 6 |
| Reliability | 3 | 5 | 15 | 4 | 12 | 4 | 12 |
| **Weighted total** | | | **44** | | **41** | | **38** |

**Обоснование весов:**
- Latency × 3 — критический путь продукта (см. [s05])
- Cost × 2 — важно, но не блокирующий
- ...

**Sensitivity:** если поменять Latency на ×2, ranking не меняется (A=37, B=38, C=34) — выбор A robust.
```

---

## C3 — `best-fit-when`

**Когда:** Decision всегда. Для каждой опции — условия, при которых она правильная.

**Что внутри:** Для каждой опции набор условий «бери если...».

**Антипаттерн:** «X лучше всегда» — почти никогда не правда. Каждая опция оптимальна в каких-то условиях.

**Композиция:** После `options-matrix` или `weighted-score`. До `trade-offs`.

**Шаблон:**

```markdown
## Best fit when

### Option A — бери если:
- Critical path = latency
- Команда уже знакома со стеком A
- Готов принять <trade-off>
- Бюджет ≥ X

### Option B — бери если:
- Critical path = cost
- Это MVP или ранняя стадия
- Команда смешанная, нужна низкая порог входа
- Можно жить с <trade-off>

### Option C — бери если:
- Нужно избежать vendor lock-in
- Регулятор требует <constraint>
- ...
```

---

## C4 — `reversibility-stakes`

**Когда:** Decision. Особенно high-stakes и сложно-обратимые.

**Что внутри:** Reversibility (one-way vs two-way door по Безосу) + stakes уровень + что нужно для отката.

**Антипаттерн:** Не оценить reversibility — главная причина регрета. Two-way door можно решать быстро, one-way — никогда.

**Композиция:** После `options-matrix`. До `recommendation-conditional`.

**Шаблон:**

```markdown
## Reversibility & stakes

### Option A
- **Reversibility:** two-way door (можно откатиться за <время>)
- **Stakes:** medium
- **Что нужно для отката:** <конкретные действия + стоимость>
- **Точка невозврата:** <когда становится one-way>

### Option B
- **Reversibility:** one-way door
- **Stakes:** high
- **Что нужно для отката:** только rebuild с нуля, ~<время> ~$<стоимость>
- **Mitigation:** делать pilot на 10% перед full commit

### Option C
- **Reversibility:** two-way door
- **Stakes:** low
- **Что нужно для отката:** trivial
```

---

## C5 — `trade-offs`

**Когда:** Decision всегда. Честный разговор о том, что теряешь выбирая каждый вариант.

**Что внутри:** Для каждой опции — что НЕ получаешь, чего лишаешься.

**Антипаттерн:** Слабые trade-offs («есть некоторые сложности»). Каждый trade-off — конкретный с цифрой если возможно.

**Композиция:** После `best-fit-when`. До `recommendation-conditional`.

**Шаблон:**

```markdown
## Trade-offs (honest)

### Выбирая A — теряешь:
- B-экосистему интеграций (~50 готовых connectors)
- Опыт команды в Y (есть кривая обучения ~3 месяца)
- <конкретное число / факт>

### Выбирая B — теряешь:
- Latency advantage (B на 80ms медленнее в P95) [s07]
- Гибкость кастомизации
- Long-term cost optimization (B vendor-locked, рост цен 15% YoY)

### Выбирая C — теряешь:
- Community и docs (C маленький проект, документации мало)
- Hiring pool (мало кто умеет)
```

---

## C6 — `recommendation-conditional`

**Когда:** Decision финальный блок. Чёткая рекомендация с условиями.

**Что внутри:** «Бери X если Y, иначе Z» — формат для разных условий.

**Антипаттерн:** «Зависит от обстоятельств» без перечисления обстоятельств. Если зависит — перечисли явно от чего.

**Композиция:** После всех сравнительных блоков. До `actionable-next-steps`.

**Шаблон:**

```markdown
## Рекомендация

**Бери A**, если выполнено хотя бы 2 из 3:
- Latency = critical path
- Команда ≥ 5 человек с опытом в Y
- Бюджет ≥ $X в месяц

**Иначе бери B**, если:
- MVP / ранняя стадия
- Бюджет < $X
- Готов принять <trade-off>

**Иначе бери C** (default fallback):
- Не подходит A и B
- Нужна максимальная independent control

**Когда рекомендация меняется:**
- Если латентность перестанет быть критичной → A снимается с лидерства
- Если появится регулятор Z в нашей юрисдикции → C поднимается
- Если будет $X+ funding → A становится default
```

---

## C7 — `pre-mortem`

**Когда:** Decision high-stakes. Перед commit к решению.

**Что внутри:** «Представь что через год решение провалилось — почему?» Список причин провала.

**Антипаттерн:** Поверхностный список («баги случаются»). Каждая причина — конкретный механизм провала.

**Композиция:** До `recommendation-conditional` — может изменить рекомендацию.

**Шаблон:**

```markdown
## Pre-mortem

**Сценарий:** через 12 месяцев решение признано провалившимся. Возможные причины:

### Сценарий A: <технический провал>
**Что произошло:** <конкретный механизм>
**Вероятность:** low | medium | high
**Mitigation:** <что можно сделать заранее>
**Indicators (что предупредит заранее):** ...

### Сценарий B: <провал команды>
**Что произошло:** ...
**Вероятность:** ...

### Сценарий C: <market shift>
...

### Сценарий D: <vendor / partner>
...

**Самый страшный сценарий:** <конкретный>. Mitigation: <что должны сделать ДО старта>.
```

---

## C8 — `cost-benefit`

**Когда:** Custom для финансовых решений или time-investment. Любых где есть явные costs и benefits в сравнимых единицах.

**Что внутри:** Структурированный cost vs benefit с allowed ranges.

**Антипаттерн:** Считать только tangible costs без opportunity cost. Время — тоже cost.

**Композиция:** Для финансовых решений вместо `options-matrix` или дополнением.

**Шаблон:**

```markdown
## Cost-benefit

### Costs (за <период>)

| Категория | Low estimate | High estimate | Источник |
|---|---|---|---|
| Time | 80 hours | 160 hours | <обоснование> |
| Money direct | $5000 | $12000 | [s03] |
| Opportunity cost | <что не сделаешь> | <что не сделаешь> | — |
| **Total** | **$X** | **$Y** | |

### Benefits (за <период>)

| Категория | Low | High | Confidence | Источник |
|---|---|---|---|---|
| Revenue uplift | $10k | $50k | medium | [s07] |
| Time saved | 100h | 300h | high | [s11] |
| Strategic value | — | — | low (qualitative) | — |

### Net
- **Pessimistic (low benefits, high costs):** -$2k = net negative
- **Realistic (mid):** +$15k
- **Optimistic (high benefits, low costs):** +$50k

### Break-even
- Точка безубыточности: <условие>
- Time to break-even: <месяцы>
```

---

## C9 — `pros-cons-each`

**Когда:** Quick decision, light-weight отчёты. Когда матрица overkill.

**Что внутри:** Pro/Con списки для каждой опции.

**Антипаттерн:** Не использовать в high-stakes ресёрчах — слишком поверхностно. Для quick takes.

**Композиция:** Альтернатива `options-matrix` для shallow decision-ресёрчей.

**Шаблон:**

```markdown
## Pros & Cons

### Option A
**Pros:**
- ✅ ... [s03]
- ✅ ...
- ✅ ...

**Cons:**
- ❌ ... [s07]
- ❌ ...

### Option B
**Pros:**
- ✅ ...
- ✅ ...

**Cons:**
- ❌ ...
- ❌ ...
```

---

## C10 — `feature-matrix`

**Когда:** Product comparison. Когда сравниваем продукты по наличию фич.

**Что внутри:** Features × Products таблица (✅ есть / ❌ нет / 🟡 частично / 💰 платно).

**Антипаттерн:** Длинный список фич без приоритизации. Фичи делятся на core (must-have) и nice-to-have.

**Композиция:** Дополнение к `options-matrix` для product decision. После него.

**Шаблон:**

```markdown
## Feature matrix

### Core features (must-have)

| Feature | Product A | Product B | Product C |
|---|---|---|---|
| <feature 1> | ✅ | ✅ | 🟡 partial |
| <feature 2> | ✅ | ❌ | ✅ |
| <feature 3> | 💰 paid only | ✅ | ✅ |
| <feature 4> | ✅ | ✅ | ❌ |

### Nice-to-have

| Feature | A | B | C |
|---|---|---|---|
| <feature 5> | ✅ | ❌ | ❌ |
| <feature 6> | 🟡 | ✅ | ✅ |

**Coverage:**
- A: 4/4 core (75% all)
- B: 3/4 core (62% all)
- C: 3/4 core (62% all)
```

---

## C11 — `migration-path`

**Когда:** Decision где обратимость возможна но требует усилий. «Если A не зайдёт, как мигрировать на B?»

**Что внутри:** Шаги миграции A→B с временем и риском.

**Антипаттерн:** Скрывать миграционные costs. Они часть decision.

**Композиция:** После `reversibility-stakes`. Конкретизирует обратимость.

**Шаблон:**

```markdown
## Migration paths

### A → B (если решение A не зайдёт)
1. **Подготовка** (~<время>): <что нужно сделать>
2. **Pilot миграция** (~<время>): <часть данных/функционала>
3. **Full cutover** (~<время>): <…>
4. **Rollback option до конца**: да/нет

**Riski:**
- ⚠️ Data loss risk: low | medium | high
- ⚠️ Downtime: <время>
- ⚠️ Customer impact: ...

**Total cost:** <время> + $<стоимость>

### A → C (альтернативный path)
...
```

---

## C12 — `decision-tree`

**Когда:** Сложные мультиусловные решения. Когда «если X — A, если Y — B» — больше 2 веток.

**Что внутри:** ASCII-дерево решений или текстовая структура.

**Антипаттерн:** Дерево с >7 листьями — становится нечитаемым. Если так — упрости вопрос или разбей на 2 дерева.

**Композиция:** Может заменить `recommendation-conditional` для сложных случаев. Или дополнить.

**Шаблон:**

```markdown
## Decision tree

```
Q1: Это high-stakes решение (revert >$50k)?
├─ Yes: Q2: Регулируемый домен?
│       ├─ Yes → Option C (compliance-first)
│       └─ No:  Q3: Команда ≥ 5 senior?
│               ├─ Yes → Option A
│               └─ No  → Option B (managed service)
└─ No:  Q4: Latency critical?
        ├─ Yes → Option A (regardless of size)
        └─ No  → Option B (cheaper, simpler)
```

**Обоснование узлов:**
- Q1 stakes threshold $50k обоснован: [s05]
- Q3 «5 senior» — практическое наблюдение: [s11]
```

---

## C13 — `kill-criteria`

**Когда:** Decision для рискованных решений. «Когда отказаться от каждой опции».

**Что внутри:** Для каждой опции — индикаторы, при которых нужно убить её и переключиться.

**Антипаттерн:** Sunk cost — продолжать с опцией после явных kill-signals. Kill criteria должны быть pre-stated.

**Композиция:** После `recommendation-conditional`. До `actionable-next-steps`.

**Шаблон:**

```markdown
## Kill criteria

### Option A — kill if:
- Latency не улучшилась после <effort> work
- Cost overruns >50% от estimate
- 2+ месяца до production без видимого прогресса
- **Then:** мигрируй на B по migration-path выше

### Option B — kill if:
- Vendor поднял цены >30%
- API стал unstable (>5 breaking changes в год)
- **Then:** мигрируй на A с budget allocation

### Option C — kill if:
- Compliance перестало быть constraint
- **Then:** свобода выбора между A и B
```
