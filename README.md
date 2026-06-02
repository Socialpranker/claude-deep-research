<div align="center">

# Deep Research

### A structured meta-research skill for Claude Code

**Stop ad-hoc Googling. Start documented investigation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-d97757?style=flat-square)](https://claude.com/claude-code)
[![Skills](https://img.shields.io/badge/Anthropic-Agent%20Skills-d97757?style=flat-square)](https://docs.anthropic.com/claude/docs/skills)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)
[![Auto-Validated](https://img.shields.io/badge/APIs-Auto--Validated%20Weekly-blueviolet?style=flat-square)](.github/workflows/catalog-sync.yml)
[![Stars](https://img.shields.io/github/stars/Socialpranker/claude-deep-research?style=flat-square&logo=github)](https://github.com/Socialpranker/claude-deep-research/stargazers)

<br>

**[Docs](https://socialpranker.github.io/claude-deep-research/)** · **[Install](#install-in-30-seconds)** · **[How it works](#how-it-works)** · **[Contribute](CONTRIBUTING.md)**

<br>

```
You: investigate the trade-offs between Postgres logical replication and CDC tooling

Claude:  ✓ Reframed your question (3 hypotheses)
         ✓ Picked genre: decision (comparison + validation)
         ✓ Wrote plan.md (17 sections)
         ✓ Checked your env: 4 APIs available, 2 fallback to HTML
         ✓ Launched 4 sub-agents across 12 channels
         ✓ Saved 23 sources to sources/ with quotes
         ✓ Ran adversarial pass (3 counter-arguments)
         ✓ Report ready: research/postgres-replication-vs-cdc/2026-05-21_decision.md
```

</div>

---

## What this is

A [Claude Code skill](https://docs.anthropic.com/claude/docs/skills) that turns **"research this topic"** into a **7-phase pipeline** with hypothesis testing, parallel sub-agent search, source triangulation, and adversarial review.

The output is a folder you can return to in a month. Every claim traces to a specific source file. The plan documents *why* you made every choice. No re-research needed.

<table>
<tr>
<th width="50%">Without this</th>
<th width="50%">With this</th>
</tr>
<tr>
<td>

One-shot prompt → wall of text

Sources lost in chat history

No way to detect bias

No reuse next time

Generic Google results

Sources include... *(vague)*

</td>
<td>

17-section `plan.md` documents every choice

Each source = file with verbatim quotes

Mandatory adversarial pass + opposition queries

Atomic theses in `findings/FN.md` reusable

29 named channels + 280+ stat sources

Every claim → `[s12]` link → specific quote

</td>
</tr>
</table>

---

## Install in 30 seconds

<details open>
<summary><b>For Claude Code (CLI)</b></summary>

```bash
git clone https://github.com/Socialpranker/claude-deep-research.git \
  ~/.claude/skills/deep-research
```

That's it. Now type any of these in a Claude Code session:
- `/deep-research`
- "Investigate X"
- "Изучи тему"
- "Validate this hypothesis"

</details>

<details>
<summary><b>For Claude Desktop (Skills enabled)</b></summary>

```bash
# Clone
git clone https://github.com/Socialpranker/claude-deep-research.git
cd claude-deep-research

# Package as .skill bundle
zip -r ../deep-research.skill . -x ".*" -x "*.zip"

# Upload via Claude.app → Settings → Skills → Add Skill
```

</details>

<details>
<summary><b>For other LLMs (Codex, Gemini, local)</b></summary>

The 6-phase methodology is portable. Load `SKILL.md` + `references/*.md` into the LLM's context manually. Skip the sub-agent parts and use separate chat sessions per subtopic.

[Full instructions →](#use-with-other-llms-codex-gemini-etc)

</details>

---

## How it works

The skill runs **7 phases** in order:

| Phase | Name | What happens |
|:---:|:---|:---|
| **1** | **Reframing** | Restates your question; identifies the decision it supports; formulates 2-4 falsifiable hypotheses |
| **2** | **Genre** | Picks report type (`qa` / `explainer` / `decision` / `landscape` / `validation` / `custom`) + block composition |
| **3** | **Plan** | Writes `plan.md` with 17 sections: acceptance criteria, risk register, glossary, sourcing strategy per subtopic |
| **3.5** | **Capability Discovery** | Audits available API keys, maps subtopics to data sources, discovers gaps via upstream awesome-lists |
| **4** | **Search** | Launches 2-5 parallel `Explore` sub-agents across 29 channels and 280+ stat sources |
| **5** | **Score & Triangulate** | Every source rated Credibility/Recency/Bias; every claim backed by ≥3 independent sources of different types |
| **6** | **Synthesize + Adversarial** | Assembles report from blocks; runs 4 self-critique questions; documents counter-arguments with steel-man |

Every phase is **transparent**: you see what's happening, you confirm key decisions, and you get a folder you can return to.

---

## What's inside

<table>
<tr>
<td width="33%" valign="top">

### 75 Report Blocks

10 categories: **FRAME** · **EXPLAIN** · **COMPARE** · **MAP** · **VALIDATE** · **ANALYZE** · **CLOSE** · **PEOPLE** · **NUMBERS** · **CONTEXT**

Each block has its own template, anti-patterns, and composition rules.

[Block library →](references/blocks/INDEX.md)

</td>
<td width="33%" valign="top">

### 29 Search Channels

Named strategies with query patterns + paywall fallbacks:

`web-general` · `academic` · `preprint-servers` · `code-github` · `forum-discussion` · `news-current` · `industry-reports` · `regulatory-legal` · `competitive-signals` · `data-statistical-gov` · `product-analytics` · `crypto-analytics` · `api-direct` · *and more*

[Channels catalog →](references/channels.md)

</td>
<td width="33%" valign="top">

### 280+ Stat Sources

14 cross-industry + 19 industry categories. Each entry: URL · Type · Access · Quality · Limitations · Combine-with · Fallback.

Categories: `gov_macro` · `companies_public` · `crypto` · `health` · `education` · `climate_env` · `science` · 19 industries

[Sources catalog →](references/stat_sources/INDEX.md)

</td>
</tr>
<tr>
<td valign="top">

### 6 Report Genres

| Genre | When |
|:---|:---|
| `qa` | Open meta-research |
| `explainer` | "How does X work" |
| `decision` | "X or Y" |
| `landscape` | "Who's in this space" |
| `validation` | "Is X true" |
| `custom` | Hybrid, assembled per question |

[Genres →](references/genres.md)

</td>
<td valign="top">

### 30+ API Endpoints

Free no-auth APIs prioritized:

`Semantic Scholar` · `OpenAlex` · `CrossRef` · `arXiv` · `DefiLlama` · `CoinGecko` · `Reddit JSON` · `HN Algolia` · `World Bank` · `SEC EDGAR` · `ClinicalTrials.gov` · `PubMed` · `GDELT`

Auth via env vars only — skill never asks for keys inline.

[API catalog →](references/api_sources/INDEX.md)

</td>
<td valign="top">

### Weekly Auto-Sync

GitHub Actions cron validates all endpoints + discovers upstream additions:

- HEAD-check 30+ APIs weekly
- Scan public-apis & awesome-public-datasets
- Auto-PR for dead endpoints
- Reports committed to `reports/` branch

[Workflow →](.github/workflows/catalog-sync.yml)

</td>
</tr>
</table>

---

## Example folder

Sample output for a typical `decision`-genre research:

```
research/<topic-slug>/
├── plan.md                              # 17-section plan
├── sources.csv                          # Index with C/R/B scoring
├── sources/                             # One file per source
│   ├── 01_vendor-docs.md                # Primary, total=14
│   ├── 02_benchmark-paper.md            # Academic, total=12
│   ├── 03_industry-report.md            # Industry, total=13
│   ├── 04_forum-thread.md               # Forum, total=9 (opposition)
│   └── ... (19 more)
├── findings/
│   ├── F1_<atomic-thesis>.md            # confidence: high
│   └── F2_<atomic-thesis>.md            # confidence: medium
└── 2026-05-21_decision.md               # Final report
```

Final report structure (assembled from the blocks chosen in plan.md):

```markdown
## TL;DR
- Claim A holds under condition X [confidence: high]
- Claim B holds conditionally on threshold Y [confidence: medium]
- Claim C is disputed by opposition sources [confidence: low]

## Mental model
[How the underlying mechanism works...]

## Falsification criteria
What would disprove H1, H2, H3...

## Verdict conditional
Recommendation IF: <conditions met>
Different recommendation OTHERWISE: <conditions broken>

## Counter-arguments (steel-man)
CA1: "<the strongest opposing claim>" [source: s09]
     → Our answer: <conditions under which CA1 fails>
CA2: ...
```

Every claim is clickable to its source. A month later, you don't re-research — you read.

---

## Contribute

The catalog is most valuable when **it grows**. Easy contributions:

| Time | Type | Example |
|:---:|:---|:---|
| 15 min | Add a stat source | `Add SimilarWeb Pro to consumer_digital` |
| 15 min | Improve a query pattern | `Better arxiv channel queries for biology` |
| 30 min | New search channel | `Add patent-search with USPTO+EPO fallback` |
| 1-2h | New industry category | `Add industries/aerospace.md` |
| 2-4h | New report block | `Add decision-tree to compare.md` |
| Half-day | LLM adapter | `Add codex/ folder with adapted protocols` |

[Full contributing guide →](CONTRIBUTING.md)

[![Contributors](https://contrib.rocks/image?repo=Socialpranker/claude-deep-research)](https://github.com/Socialpranker/claude-deep-research/graphs/contributors)

---

## FAQ

<details>
<summary><b>How is this different from ChatGPT Deep Research / Perplexity?</b></summary>

Those are **products** — closed UI, fixed flow, opaque source selection. This is **open methodology** — you control every step, the protocol is markdown you can fork, the source catalog is yours to extend.

They also don't separate sources into files, don't do explicit triangulation, don't run adversarial passes, and don't produce reusable atomic theses.

</details>

<details>
<summary><b>Does it work without Claude Code CLI?</b></summary>

Yes — on Claude Desktop with Skills enabled. Also works manually with any LLM by loading the markdown files into context (see ["Use with other LLMs"](#use-with-other-llms-codex-gemini-etc) below).

</details>

<details>
<summary><b>What's a research output look like?</b></summary>

See the [example folder](#example-folder) above. TL;DR: a folder with `plan.md` + `sources/NN.md` per source + `findings/FN.md` atomic theses + final `<date>_<genre>.md` report.

Every claim in the final report links to a specific `sources/NN.md` file.

</details>

<details>
<summary><b>Why so many files? Isn't this overkill?</b></summary>

For a 5-minute "what's the latest X" question — yes. That's why `shallow` mode exists (5-7 sources, no sub-agents, ~15 min). The full machinery is for `medium` (1 hour) and `deep` (3 hours) when you need to actually use the output for a decision.

The file-per-source structure is the key **reuse** mechanism. A single research often informs 3-5 future researches because you can cite individual `sources/NN.md` directly.

</details>

<details>
<summary><b>Is this just prompt engineering?</b></summary>

It's **structured methodology + curated catalog + reusable templates + automation**.

- The 7-phase workflow forces discipline
- 280+ stat sources catalog is curated knowledge
- 75 reusable blocks compose any report shape
- Weekly auto-validation keeps the catalog alive
- 25+ upstream awesome-lists give infinite discovery layer

Prompts are an implementation detail, not the value.

</details>

<details>
<summary><b>Can I use this commercially?</b></summary>

Yes — MIT licensed. Use it, modify it, integrate it into products. Attribution appreciated but not required.

</details>

---

### Use with other LLMs (Codex, Gemini, etc.)

The methodology is portable. ~70% of content is LLM-agnostic markdown templates.

| Component | Claude-specific | Universal |
|:---|:---:|:---:|
| `SKILL.md` frontmatter | ✓ | — |
| Sub-agent `Explore` type | ✓ | — |
| 7-phase workflow | — | ✓ |
| 75 report blocks | — | ✓ |
| 29 search channels | — | ✓ |
| 280+ stat sources | — | ✓ |

**To adapt:**
1. Load `SKILL.md` + relevant `references/*.md` into the LLM's context
2. Replace sub-agent parallelism with separate chat sessions per subtopic
3. Manage source files (`sources/NN.md`) externally — LLM produces content
4. PRs welcome for `codex/`, `gemini/`, `local/` adapters

---

<div align="center">

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Socialpranker/claude-deep-research&type=Date)](https://star-history.com/#Socialpranker/claude-deep-research&Date)

</div>

---

<details>
<summary><h2>На русском</h2></summary>

**Deep Research** — скилл для [Claude Code](https://claude.com/claude-code), превращающий «загугли это» в дисциплинированный 7-фазный процесс.

### Что внутри

- **7 фаз workflow**: Reframing → Genre → Plan → Capability Discovery → Search → Score → Synthesis
- **6 жанров отчёта**: qa / explainer / decision / landscape / validation / custom
- **75 блоков** в 10 категориях — переиспользуемые секции с шаблонами и анти-паттернами
- **29 каналов поиска** с paywall fallback протоколом (включая api-direct)
- **280+ статистических источников** в 14 cross-industry + 19 отраслевых категориях
- **30+ API endpoints** для programmatic доступа (free no-auth приоритетны)
- **plan.md** с 17 секциями для прозрачности
- **Adversarial pass** с 4 вопросами самокритики (обязателен для medium/deep)
- **Weekly auto-validation** через GitHub Actions

### Установка

```bash
git clone https://github.com/Socialpranker/claude-deep-research.git ~/.claude/skills/deep-research
```

Триггеры: «проведи ресёрч», «изучи тему», «копни глубоко», `/deep-research`

### Вклад

Каталог растёт через PRs. Самые ценные — новые источники в `stat_sources/` и `api_sources/`. См. [CONTRIBUTING.md](CONTRIBUTING.md).

</details>

---

<div align="center">

### Built by [Socialpranker](https://github.com/Socialpranker) · [MIT License](LICENSE) · [Roadmap](https://github.com/Socialpranker/claude-deep-research/discussions)

**If this skill saves you time, [give it a star](https://github.com/Socialpranker/claude-deep-research)** — it's the only metric I check.

</div>
