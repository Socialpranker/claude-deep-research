# Phase 5 — Scoring + Triangulation (design)

**Дата:** 2026-06-15
**Статус:** дизайн утверждён, реализация не начата
**Фаза:** Phase 5 по нумерации README (Scoring + triangulation) — НЕ путать с
«Phase 5 Stage 1/2» из коммитов (это этапы живого web_search внутри Phase 4).

## Проблема

`Orchestrator.run()` ([runner/orchestrator.py:175](../../../runner/orchestrator.py))
гоняет фазы 1→2→3→4→6, пропуская Phase 5. В результате:

- Источники из Phase 4 не оценены: `sources/NN.md` содержит лишь
  `id/url/title/access/type`, причём `type` — заглушка
  (`stype = "Primary" if written % 2 else "Academic"`, не выведен из источника).
- Триангуляция гипотез не проверяется — нет сигнала «тезис стоит на одном голосе».
- `TODO(Phase 5)` в [runner/adaptive.py:262](../../../runner/adaptive.py) ждёт
  backfill: для `pursued` deviations поля забиты заглушками
  `outcome="(pending scoring)"`, `new_source_ids=[]`.

Phase 5 — связующее звено: её ждёт backfill из Phase 4 (назад), и от неё
зависит достоверность синтеза в Phase 6 (вперёд).

## Решения (резолв развилок брейншторма)

1. **Природа scoring:** живая LLM-оценка с первого дня (не детерминированный
   scaffold). Согласуется с тем, как сделана Phase 4 (живой web_search).
2. **Граница фазы:** Phase 5 заполняет ТОЛЬКО выводимое из `url+title+claim` —
   scoring (credibility/recency/bias/total), `type` (из 7), `hypothesis_evidence`.
   Мета-поля источника (`author/date/channel/language/fetched`) НЕ трогаем —
   это отдельная задача Phase 4-fetch. Phase 5 не галлюцинирует то, чего нет.
3. **Триангуляция считается по гипотезам H1–H4**, а не по тезисам отчёта
   (тезисы рождаются в Phase 6, в Phase 5 их ещё нет). Использует
   `s.hypotheses` + `hypothesis_evidence` из шага scoring.
4. **Структура кода:** один метод `Orchestrator.score(s)` (подход A — повторяет
   паттерн `search()`), не отдельный модуль. Модуль выделим позже, если метод
   разрастётся.

## Архитектура

Новый метод `Orchestrator.score(s: RunState) -> None`, вызывается в `run()`
между `search()` и `synthesize()`:

```python
def run(self, question, depth, root):
    s = RunState(question=question, depth=depth, root=root)
    self.reframe(s)
    self.choose_genre(s)
    self.plan(s)
    self.search(s)
    self.score(s)        # ← Phase 5 (новое)
    self.synthesize(s)
    return s.dir
```

`score()` — три внутренних шага по порядку (в одном методе, паттерн `search()`):

### Шаг 1 — Per-source scoring (`model_tier="cheap"` → haiku)

Один batched-вызов `self.p.complete(...)` на все источники прогона. Вход:
`[{id, url, title, claim}]` + список гипотез. Выход — structured JSON:

```python
SCORE_SCHEMA = {
  "sources": [{
    "id": "s01",
    "credibility": 1-5,   # рубрика references/source_scoring.md
    "recency": 1-5,
    "bias": 1-5,
    "type": "Primary|Academic|Industry-media|General-media|Expert-blog|Forum|Other",
    "hypothesis_evidence": { "H1": "supports|contradicts|partial|neutral", ... }
  }]
}
```

- `total = credibility + recency + bias` считается в Python (модели не доверяем
  арифметику; диапазон 3–15).
- `id`, которого нет в `s.sources`, игнорируется (защита от галлюцинации id).

### Шаг 2 — Triangulation (`model_tier="mid"` → sonnet)

Вход — агрегат «гипотеза → какие источники supports/contradicts и каких типов»
(строится в Python из результата шага 1). Выход:

```python
TRIANGULATION_SCHEMA = {
  "hypotheses": [{
    "id": "H1",
    "distinct_types_supporting": int,     # число РАЗНЫХ type среди supports
    "distinct_types_contradicting": int,
    "under_triangulated": bool,           # True если supporting < 3 разных типов
    "note": "одна строка"
  }]
}
```

Правило триангуляции (references/source_scoring.md): тезис обоснован, если его
поддерживают ≥3 независимых источника РАЗНОГО типа. `under_triangulated=True` →
сигнал для Phase 6.

### Шаг 3 — Persist + backfill

| Файл | Изменение |
|---|---|
| `sources/NN_sid.md` | frontmatter получает `credibility, recency, bias, total, type` (реальный), `hypothesis_evidence`. Существующие `id/url/title/access` сохраняются. Мета-поля НЕ добавляем. |
| `sources.csv` | колонки: `id,title,url,type,credibility,recency,bias,total,used` (9 шт.). |
| `triangulation.md` | НОВЫЙ файл — таблица H1–H4 × разнотипные голоса + флаг under-triangulated + note. Вход для Phase 6. |
| `deviations.md` | перезаписывается с backfill `outcome`/`new_source_ids`. |

## Backfill deviations (закрытие TODO adaptive.py:262)

Подход B1: в `search()` запоминать `round_index → [source_ids]` (дешёвый словарь,
данные уже под рукой при сборе источников). Тогда `score()` заполняет:
- `new_source_ids` — точный список id, пришедших из round этой deviation;
- `outcome` — краткий агрегат (напр. `"3 sources, avg total 11"`).

Меняет `search()` минимально (добавить учёт round→ids при записи источников).
Альтернатива B2 (только `outcome`, `new_source_ids=[]`) отвергнута — оставляет
TODO наполовину открытым.

## Обработка ошибок

Паттерн уже есть в `search()`:

- **DryRunProvider** → детерминированные баллы (`credibility=3, recency=3,
  bias=3, type="Other"`, все гипотезы `neutral`) — оффлайн-тесты и CI без ключей.
- Живой провайдер вернул кривой JSON / лишний `id` / отсутствующий source →
  пропускаем источник, не валим прогон. Источник, который провайдер не оценил
  (нет записи в ответе), помечается `total: null` в frontmatter (видимый сигнал
  пропуска, не молчаливый дефолт). Это касается ТОЛЬКО живого провайдера;
  DryRun всегда возвращает полный набор баллов.
- `total` всегда из Python-суммы — модель не считает арифметику.

## Тестирование (pytest, как tests/test_adaptive.py)

- `test_scoring.py` на `DryRunProvider`: frontmatter обогащён, `total` = сумма,
  `sources.csv` имеет новые колонки, `triangulation.md` создан.
- under-triangulated кейс: гипотеза с источниками одного типа → `True`.
- backfill: `deviations.md` после `score()` содержит непустые `new_source_ids`
  для pursued deviations.
- защита: лишний `id` от провайдера игнорируется, прогон не падает.
- live-тест под `@pytest.mark.live` (skipped по умолчанию).

Верификация перед «готово»: `pytest tests/ -q` + `ruff check` (CI имеет ruff-гейт)
+ перечитать спеку построчно.

## Явные сужения относительно спеки (сознательные, не недоделки)

Следствие выбранной узкой границы фазы (только выводимое из `url+title+claim`):

- `sources.csv` — **9 колонок, не 14**. Опускаем `channel/author/date/note/file`:
  Phase 5 этих данных не имеет. Gap для будущей Phase 4-fetch.
- frontmatter источника — НЕ добавляем `author/date/channel/language/fetched`.
  Те же причины.

Эти поля spec'ом предусмотрены, но их источник — fetch реальной страницы, а не
LLM-вывод. Реализация — отдельная задача (Phase 4-fetch), вне Phase 5.

## Model routing (references/model_routing.md)

| Подзадача | tier | модель |
|---|---|---|
| Per-source scoring | `cheap` | claude-haiku-4-5 |
| Triangulation check | `mid` | claude-sonnet-4-6 |

## Зависимости

```
Phase 4 (search) ──round→ids──┐         ┌── backfill new_source_ids/outcome
                              ▼         │
                        Phase 5 (score) ─┘
                              │ triangulation.md, scored sources.csv
                              ▼
                        Phase 6 (synthesize) — читает scoring для confidence
```
