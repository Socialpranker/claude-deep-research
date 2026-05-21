# VALIDATE blocks — проверка истинности

Блоки для validation-жанра. «Правда ли X».

---

## V1 — `falsification-criteria`

**Когда:** Validation всегда. ДО просмотра evidence.

**Что внутри:** Что заставило бы признать claim ложным. Формулируется заранее — защита от confirmation bias.

**Антипаттерн:** Формулировать falsification после evidence — это уже rationalization. Pre-stated only.

**Композиция:** Сразу после `claim-precise`. До `evidence-graded`.

**Шаблон:**

```markdown
## Falsification criteria

ДО просмотра evidence фиксируем: какие данные опровергнут claim?

**Если найдём:** <конкретное observation X> → claim ЛОЖНЫЙ.
**Если найдём:** <observation Y> → claim ВЕРНЫЙ.
**Если найдём:** <observation Z> → claim условно верный (только при <условие>).

**Какое evidence нам бы было НЕДОСТАТОЧНО:**
- <тип источника / тип данных> — даже если найдём, не считаем
- <напр.: одно исследование, не воспроизведённое — недостаточно>

**Записано до начала поиска evidence:** да | нет (если нет — пометить, признать bias risk)
```

---

## V2 — `evidence-graded`

**Когда:** Validation всегда. После falsification, перед verdict.

**Что внутри:** Evidence FOR и AGAINST раздельно, каждый с quality grade A/B/C.

**Антипаттерн:** Смешивать evidence в один список. FOR/AGAINST должны быть параллельны и сравнимы.

**Композиция:** После `falsification-criteria`. До `verdict-conditional`.

**Шаблон:**

```markdown
## Evidence

### Quality grading
- **A** — peer-reviewed study, RCT, large N, replicated
- **B** — observational study, expert consensus, single-source primary
- **C** — anecdote, single expert opinion, blog post

### Evidence FOR

#### F1: <тезис в одной фразе>
**Источник:** [s03] — peer-reviewed, N=2000, 3-year follow-up
**Что говорит:** ...
**Quality:** A
**Scope:** где, когда, на ком исследование
**Limitations:** ...

#### F2: <тезис>
**Источник:** [s07]
**Quality:** B (observational)
...

#### F3: ...

### Evidence AGAINST

#### A1: <тезис в одной фразе>
**Источник:** [s11] — meta-analysis of 14 studies
**Что говорит:** ...
**Quality:** A
**Scope:** ...

#### A2: ...

### Weight summary
- FOR: 3 A-grade + 4 B-grade + 1 C-grade
- AGAINST: 1 A-grade + 2 B-grade
- **Balance:** evidence weighted toward FOR, но A против — серьёзно
```

---

## V3 — `conflicting-evidence`

**Когда:** Validation когда есть прямо противоречащие источники.

**Что внутри:** Случаи где данные говорят X, и где ¬X. Анализ почему расходятся.

**Антипаттерн:** Скрывать конфликты. Конфликт сам по себе — важная информация.

**Композиция:** После `evidence-graded`. До `verdict-conditional`.

**Шаблон:**

```markdown
## Conflicting evidence

### Conflict 1: <тема>
**Side A says:** ... [s05]
**Side B says:** ... [s11]
**Почему расходятся:**
- Different populations (A в группе X, B в группе Y)
- Different methodology (RCT vs observational)
- Conflict of interest (B funded by Z)
- Time period (A 2018, B 2024 — могло измениться)

**Что более вероятно правда:** <обоснование>
**Confidence в этом разрешении:** medium

### Conflict 2: ...
```

---

## V4 — `base-rates`

**Когда:** Validation медицинских/научных/probabilistic claims. Где есть baseline вероятность.

**Что внутри:** Apriori probability + почему она такая.

**Антипаттерн:** Игнорировать base rate. Bayesian reasoning требует prior.

**Композиция:** Перед `evidence-graded`. Контекст для оценки силы evidence.

**Шаблон:**

```markdown
## Base rates (prior probability)

**Claim:** «X вызывает Y».

**Базовая частота Y в общей популяции:** ~Z% [s05]
**Базовая частота Y у людей с X:** ~W% [s07]
**Разница (effect size):** W - Z = <X percentage points>

**Что это значит для prior:**
- Если W ≈ Z → нет видимого эффекта в наблюдательных данных
- Если W >> Z → strong correlation, но всё ещё нужна caustality

**Confounders которые могут объяснить разницу:**
- Age (people with X are older on average)
- Lifestyle
- Selection bias (only certain types report X)

**Prior probability claim верен (наша оценка до evidence):** ~30%.
```

---

## V5 — `verdict-conditional`

**Когда:** Validation всегда. Финальный verdict.

**Что внутри:** Verdict с conditional модификациями — «правда при X, ложь при Y, недостаточно при Z».

**Антипаттерн:** Бинарный verdict (true/false) когда реально conditional. Большинство claims conditional.

**Композиция:** После всех evidence-блоков. До `closing` секции.

**Шаблон:**

```markdown
## Verdict

**Overall:** confirmed | partially confirmed | contradicted | inconclusive
**Confidence:** high | medium | low

### Unconditional verdict

<если применимо: «Claim верен» или «Claim ложен» с одной фразой обоснования>

### Conditional verdict (если применимо)

- **Верно ПРИ условии:** <X>
- **Ложно при:** <Y>
- **Недостаточно данных для:** <Z scenario>

### Scope verdict
- **В контексте X:** confirmed
- **В контексте Y:** unclear (надо больше данных)
- **В контексте Z:** contradicted

### Что вошло в verdict
- Evidence FOR — A-grade: <count>, B-grade: <count>
- Evidence AGAINST — A-grade: <count>, B-grade: <count>
- Falsification criteria: <выполнены? нарушены?>
- Base rate consideration: <учтена>

### Что НЕ вошло (deliberately excluded)
- C-grade anecdotes (по дисциплине quality cutoff)
- Sources с известным conflict of interest без раскрытия
```

---

## V6 — `what-would-change-verdict`

**Когда:** Validation после verdict. Что бы заставило пересмотреть.

**Что внутри:** Конкретные типы данных, которые сдвинули бы verdict в любую сторону.

**Антипаттерн:** «Больше исследований» без конкретики. Уточняй — какие именно исследования, какого дизайна.

**Композиция:** После `verdict-conditional`. До `closing`.

**Шаблон:**

```markdown
## What would change the verdict

**Verdict вырос бы (с medium до high confidence)**, если бы появилось:
- <тип study X с N >= ...>
- Replication в <country/population>
- Mechanism elucidation (mechanistic study)

**Verdict упал бы (с confirmed до contradicted)**, если бы:
- <тип evidence>
- Retraction <s03>
- Counter-RCT с эффектом opposite

**Verdict не изменится** от:
- Ещё anecdotal evidence (qualitative ceiling reached)
- Ещё observational без causation
- Marketing materials
```

---

## V7 — `replication-status`

**Когда:** Научный validation. Проверка воспроизводимости.

**Что внутри:** Воспроизведён ли результат, кем, сколько раз.

**Антипаттерн:** Полагаться на одно исследование. Replication crisis показывает что нужно ≥2-3.

**Композиция:** Дополнение к `evidence-graded`. Один из quality factors.

**Шаблон:**

```markdown
## Replication status

### Оригинальное исследование
- **Citation:** [s03]
- **Year:** 2018
- **N:** 250
- **Method:** RCT, double-blind, placebo-controlled

### Replications

| Year | Citation | N | Independent? | Result |
|---|---|---|---|---|
| 2019 | [s05] | 180 | yes (diff lab) | ✅ replicated |
| 2020 | [s07] | 500 | yes (diff country) | 🟡 partial replication (effect smaller) |
| 2022 | [s11] | 300 | no (same lab) | ✅ replicated (但 same authors) |
| 2023 | [s14] | 800 | yes | ❌ failed to replicate |

### Status
- **Independent replications:** 2 successful, 1 failed
- **Confidence in original:** medium (mixed replication)
- **Meta-analysis available:** [s17] pooling N=2030, effect size <X>

### Replication signals
- Pre-registration: <yes/no/some>
- Open data: <yes/no/some>
- Conflict of interest declared: <yes/no/some>
```

---

## V8 — `sample-size-analysis`

**Когда:** Quantitative validation. Когда размер выборки критичен.

**Что внутри:** N в каждом источнике, statistical power, что значит для confidence.

**Антипаттерн:** Игнорировать малые N. Study с N=20 не базис для confident verdict.

**Композиция:** Дополнение к `evidence-graded`. Quality detail.

**Шаблон:**

```markdown
## Sample size analysis

| Источник | N | Power (если known) | Notes |
|---|---|---|---|
| [s03] | 250 | 0.8 (calculated for d=0.3) | adequate for moderate effect |
| [s05] | 50 | underpowered for small effects | could miss real but small effect |
| [s07] | 2000 | very high power | overall trustworthy |
| [s11] | 18 | severely underpowered | results suggestive only |

### Aggregate N
- Total participants across A-grade studies: ~2300
- Total across B-grade: ~400

### Power considerations
- Small effect (d=0.2) detectable: needs N≥350
- Medium effect (d=0.5) detectable: needs N≥65
- В studies adequate для medium effect, marginal для small

### Significance vs significance
- Statistical significance ≠ practical significance
- Effect size в реальных единицах: <X% change в outcome>
- Это clinical/practical значимо? <yes/no/depends>
```

---

## V9 — `methodology-critique`

**Когда:** Validation научных claims с серьёзной методологической глубиной.

**Что внутри:** Критика методологии ключевых источников.

**Антипаттерн:** Принимать peer-review как finality. Peer-review не ловит все проблемы.

**Композиция:** Дополнение к `evidence-graded`. Глубокая критика.

**Шаблон:**

```markdown
## Methodology critique

### [s03] — главное FOR-источник
**Design:** RCT, N=250
**Strengths:**
- Pre-registered
- Blinded both ways
- Adequate power for stated effect

**Weaknesses:**
- Selection bias risk: только <demographics>, не generalizes
- Outcome measure subjective (self-report)
- 18-month follow-up — могло измениться long-term
- Funding: <source> — potential conflict

**Verdict on study:** strong but limited generalizability

### [s11] — главное AGAINST-источник
**Design:** Observational, N=800
**Strengths:**
...
**Weaknesses:**
- No controls for confounders (age, lifestyle)
- Voluntary participation → selection bias
- ...

**Verdict:** suggestive but not definitive

### Common methodological issues в области
- <pattern 1>
- <pattern 2>
```

---

## V10 — `bayesian-update`

**Когда:** Probabilistic validation. Когда есть prior и evidence для update.

**Что внутри:** Prior → posterior calculation с likelihood ratios.

**Антипаттерн:** Хардкорная Bayesian math без обоснования. Это для read-friendly verdict.

**Композиция:** После `evidence-graded`. Дополнение к `verdict-conditional`.

**Шаблон:**

```markdown
## Bayesian update

### Prior
- P(claim верен) до evidence: ~30% (см. `base-rates`)

### Evidence likelihoods

| Evidence | P(E | claim) | P(E | ¬claim) | LR |
|---|---|---|---|
| F1 (RCT positive) | 0.7 | 0.2 | 3.5 |
| F2 (replication) | 0.6 | 0.3 | 2.0 |
| A1 (failed replication) | 0.3 | 0.7 | 0.43 |

### Calculation

```
Prior odds = 0.30 / 0.70 = 0.43
× LR(F1) × LR(F2) × LR(A1) = 0.43 × 3.5 × 2.0 × 0.43
≈ 1.29 (posterior odds)

Posterior probability = 1.29 / (1 + 1.29) ≈ 56%
```

### Posterior
- **P(claim верен) после evidence:** ~56%
- **Movement from prior:** +26 percentage points
- **Confidence:** medium (close to 50/50, sensitive to LR estimates)

### Sensitivity
- Если LR(F1) пересмотреть до 2.0 → posterior 38%
- Если добавить ещё одно failed replication → posterior 35%
- Этот anal sensitive — verdict robust в diapason 40-65%, не больше
```
