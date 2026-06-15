# Phase 6.5 — Verify (citation checking) design

**Дата:** 2026-06-15
**Статус:** дизайн утверждён, реализация не начата
**Фаза:** Phase 6.5 по нумерации README (Verify), ПОСЛЕ Phase 6 (Synthesis).

## Проблема

`Orchestrator.synthesize()` ([runner/orchestrator.py:281](../../../runner/orchestrator.py))
пишет в финальный отчёт `<date>_<genre>.md` строку-плейсхолдер:

```
> **Citation integrity: pending — run eval/check_citations.py (Phase 6.5)**
```

Код проверки цитат уже существует — `eval/check_citations.py` (резолвит URL
источников по HTTP, считает `citation_integrity = alive/checkable`, помечает
red flags), но к оркестратору НЕ подключён. Phase 6.5 подключает его и заменяет
плейсхолдер реальной метрикой.

## Решения (резолв развилок брейншторма)

1. **Вызов — subprocess.** `check_citations.py` существует только как CLI
   (argparse `main()`, реальные HTTP-запросы через `requests`). Зовём его как
   subprocess — точно как уже делает `eval/score_run.py:56`. НЕ рефакторим
   eval-код (CI `.github/workflows/validate.yml` и `score_run.py` продолжают
   звать его как CLI). Переиспользуем как чёрный ящик.
2. **Best-effort, устойчивость к сбою.** `check_citations.py` делает реальные
   HTTP-запросы; верификация по природе зависит от живости внешних URL. verify()
   зовёт subprocess БЕЗ `check=True`; при любом сбое (нет сети, checker упал,
   нет/битый JSON) пишет «verification unavailable» в отчёт и НЕ валит прогон.
3. **Разделение чистой логики и subprocess.** `runner/verify.py` —
   `render_verification(citations: dict | None) -> str` (чистая, тестируется
   инъекцией dict, без HTTP). `Orchestrator.verify(s)` — тонкая обёртка
   (subprocess + чтение JSON). Паттерн `scoring.py` / `capabilities.py`.
4. **Без блокировки по порогам и без red-flag-действий.** Спека
   (`references/runtime_verification.md:40-53`) предусматривает блокировку
   прогона (medium <0.70) и действия на red flags (re-search / demote claim).
   НЕ реализуем: блокировка противоречит best-effort и неинтерактивному
   оркестратору; red-flag-действия переписали бы поток синтеза. Phase 6.5 здесь
   = проверка + запись метрики, не изменение синтеза.
5. **Гейт по depth — нет.** verify() запускается на всех depth (дёшева,
   информативна), НЕ блокирует — только пишет метрику/флаги в отчёт.

## Архитектура

Новый метод `Orchestrator.verify(s: RunState) -> None`, в `run()` после
`synthesize()`:

```python
self.synthesize(s)        # Phase 6 — пишет <date>_<genre>.md с плейсхолдером
self.verify(s)            # Phase 6.5 (новое) — заменяет плейсхолдер метрикой
return s.dir
```

### Новый модуль `runner/verify.py` (чистая логика, без сети/subprocess)

```python
PLACEHOLDER = "> **Citation integrity: pending — run eval/check_citations.py (Phase 6.5)**"

def render_verification(citations: dict | None) -> str:
    """Из JSON-результата check_citations.py собирает строку-блок метрики.
    None (subprocess упал / нет файла / offline) -> 'verification unavailable'."""
```

### Метод `verify(s)` — тонкая обёртка (паттерн `score()`)

1. subprocess: `[sys.executable, <check_citations.py>, "--research-dir", str(s.dir),
   "--out", str(s.dir / ".verify" / "citations"), "--json"]`, `check=False`.
   Ловим `FileNotFoundError`/`OSError` → citations=None.
2. Прочитать `s.dir / ".verify" / "citations.json"` если есть и валиден → dict,
   иначе → None (`JSONDecodeError`/нет файла).
3. `block = render_verification(citations)`; заменить PLACEHOLDER в
   `<date>_<genre>.md` на block (read-modify-write). Если плейсхолдера нет —
   append block в конец (не теряем результат).

## Контракт данных

### Вход render_verification — JSON от check_citations.py

ПЕРВЫЙ ШАГ реализации: выписать реальный формат JSON из `check_citations.py`
ДОСЛОВНО (точки записи ~строки 179-222) — рендер опирается на фактические ключи,
не на предположение. Ожидаемая форма (подтвердить при реализации):

```python
{
  "citation_integrity": 0.91,         # alive / checkable
  "results": [{"url", "code", "red_flag", "access"}, ...]
}
```

### Выход render_verification

- `None` →
  `> **Citation integrity: verification unavailable — check_citations.py did not produce a report (offline or error).**`
- dict → блок:
  ```
  > **Citation integrity: <verified>/<total> verified · <N> red flags**
  > Verified <date> via check_citations.py · detail: .verify/citations.md
  ```
  где `verified` = достижимые не-red_flag источники, `red flags` =
  `red_flag: true` в `results`.

### Замена в отчёте

Плейсхолдер точный и уникальный (константа `PLACEHOLDER`). verify() читает
`<date>_<genre>.md`, `text.replace(PLACEHOLDER, block)`, пишет назад. Нет
плейсхолдера → append block в конец.

## Обработка ошибок (best-effort)

Всё ведёт к «unavailable», прогон не падает:
- subprocess `check=False`; `FileNotFoundError`/`OSError` → citations=None.
- JSON: нет файла / `JSONDecodeError` → None.
- Никаких исключений наружу из verify().

## Тестирование (pytest)

`tests/test_verify.py` (чистый рендер, детерминированно):
- dict с integrity+red flags → строка с числами и «verified».
- `None` → «verification unavailable».
- dict с `red_flag: true` → «1 red flag» в выводе.

`tests/test_orchestrator_verify.py` (оффлайн, БЕЗ реального HTTP):
- интеграция: положить готовый `.verify/citations.json` в s.dir, вызвать так,
  чтобы subprocess не ходил в сеть (monkeypatch subprocess.run на no-op) →
  плейсхолдер в отчёте заменён метрикой.
- graceful: нет `.verify/citations.json` (subprocess no-op, файла нет) → отчёт
  получает «verification unavailable», `run()` не падает.
- live (`@pytest.mark.live`, опционально): реальный checker на fixture-URL.

Верификация перед «готово»: `python3 -m pytest tests/ -q` + `ruff check runner/
tests/` + перечитать спеку построчно.

## Явные сужения относительно спеки (сознательные, не недоделки)

- Блокировка прогона по порогам (medium <0.70, deep 0 red flags) — НЕ реализуем
  (противоречит best-effort + неинтерактивному оркестратору).
- Действия на red flags (re-search / demote claim) — НЕ реализуем (переписали бы
  синтез). Phase 6.5 здесь = проверка + запись, отдельная задача.
- `eval/check_citations.py` НЕ трогаем — переиспользуем как CLI чёрный ящик.

## Model routing

Phase 6.5 = детерминированная (HTTP-резолв через `requests`), БЕЗ LLM/провайдера.
В отличие от Phase 5/3.5, не зовёт `self.p`. `references/model_routing.md`
помечает её `haiku/deterministic` — фактически чистый Python.

## Зависимости

```
Phase 6 (synthesize) ── <date>_<genre>.md с PLACEHOLDER ──┐
                                                          ▼
                          Phase 6.5 (verify) ── subprocess check_citations.py
                                  │             ── .verify/citations.{json,md}
                                  │             ── replace PLACEHOLDER в отчёте
                                  ▼
                              (run() возвращает s.dir)
```
