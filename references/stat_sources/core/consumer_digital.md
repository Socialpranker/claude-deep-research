# Consumer digital products — apps, web/SaaS, social/creator

Stats для mobile apps, web/SaaS products, social media creators.

## Mobile apps

### Sensor Tower
**URL:** sensortower.com/blog
**Access:** PARTIAL (blog OPEN, full reports paywall)
**What:** Mobile app stats, downloads estimates, revenue estimates, top charts
**When:** mobile app landscape, app revenue claims, store performance
**How:** Browse blog для published reports; search `site:sensortower.com <topic>`
**Quality:** B (estimates, not direct data); Freshness: monthly insights
**Limitations:** estimates can be off ±30% для smaller apps. Full reports paywalled.
**Combine with:** data.ai, Apptopia

### data.ai (formerly App Annie)
**URL:** data.ai/insights
**Access:** PARTIAL
**What:** Mobile market intelligence — downloads, revenue, engagement
**When:** alternative to Sensor Tower, cross-check
**Quality:** B (same caveats as Sensor Tower)

### AppMagic
**URL:** appmagic.rocks
**Access:** PARTIAL
**What:** Game-focused mobile stats
**When:** mobile gaming research specifically

### Apptopia
**URL:** apptopia.com/insights
**Access:** OPEN blog, full paywall
**What:** App intelligence
**When:** alternative source для mobile, often unique pulls

### Appfigures
**URL:** appfigures.com/top-apps
**Access:** PARTIAL
**What:** Top apps charts, basic data
**When:** quick lookup top apps в category

### App Store Connect (Apple)
**URL:** appstoreconnect.apple.com — requires developer account
**Access:** OWN-DATA only (no public access to others')
**What:** Own app analytics
**When:** только если ты developer

### Mobile app niche data approach
**Pattern:** Search `<app name> "MAU" OR "DAU" OR "downloads" leaked` — leaked decks часто содержат numbers.

---

## Web / SaaS / SEO

### SimilarWeb

**URL:** https://www.similarweb.com/
**Type:** Vendor
**Access:** PARTIAL (basic traffic free, deep paywall)

**What's inside:**
- Web traffic estimates per domain
- Traffic sources breakdown (direct, search, social, referral)
- Top countries
- Industry rankings
- App intelligence (separate product)

**When to use:**
- Web traffic estimates competitors
- Marketing channels breakdown
- Site comparison

**How to use:**
- Direct URL: `similarweb.com/website/<domain>`
- Top sites: `similarweb.com/top-websites`
- Search pattern: `<domain> similarweb`

**Data quality:**
- Credibility: B (estimates from panel data)
- Freshness: monthly aggregated
- Lag: ~1 month

**Limitations:**
- Estimates only, can be off significantly для smaller sites
- Panel bias
- Free tier limited

**Combine with:**
- Cloudflare Radar (network-level signals)
- Ahrefs / SEMrush (SEO-specific)

---

### BuiltWith

**URL:** https://builtwith.com/
**Type:** Vendor
**Access:** PARTIAL (basic free)

**What's inside:**
- Tech stack detection per domain
- CDN, analytics, frameworks, payment, CMS
- Historical tech changes

**When to use:**
- Competitor tech stack analysis
- Tech adoption claims

**How to use:**
- `builtwith.com/<domain>`

**Data quality:**
- Credibility: B
- Limitations: some tech invisible (server-side), free tier has ads/limits

**Combine with:**
- Wappalyzer (`wappalyzer.com`) — alternative, also OPEN partial
- Manual inspection

---

### Wappalyzer
**URL:** wappalyzer.com — **OPEN partial**. Browser extension + web tool. Alternative to BuiltWith.

### Cloudflare Radar
**URL:** radar.cloudflare.com — **OPEN**. Internet-wide traffic patterns, security trends, popular domains.
**Why useful:** Cloudflare sees significant share of internet traffic, so radar shows macro internet patterns.

### Crunchbase
См. `companies_private.md`. Web access: `crunchbase.com/organization/<co>`.

### LinkedIn Company Pages
**URL:** linkedin.com/company/<co> — **OPEN** basic (headcount range, recent hires, posts)
**When:** company size signal, hiring trend
**Limitations:** headcount range is wide buckets (1-10, 11-50, etc)

---

## SaaS reviews (G2, Capterra)

### G2
**URL:** g2.com/products/<name>
**Access:** OPEN
**What:** SaaS reviews (verified), ratings, alternatives
**When:** product comparison, customer sentiment per SaaS
**Quality:** B (reviews self-selected; G2 incentivizes some); cross-check.

### Capterra
**URL:** capterra.com/p/<id> — **OPEN**. Alternative to G2.

### TrustRadius
**URL:** trustradius.com/products/<name> — **OPEN**. Enterprise-focused reviews.

### Product Hunt
**URL:** producthunt.com/products/<name> — **OPEN**. Launch data, upvotes, hunters.
**When:** new product launches, early traction signal.

---

## Glassdoor (employer side)

### Glassdoor
**URL:** glassdoor.com/Reviews/<co>
**Access:** OPEN basic, deep PARTIAL
**What:** Employee reviews, interview questions, salary self-reports
**When:** team-org block, culture signals, salary benchmarks
**Quality:** C (self-selected reviews, recall bias)

---

## SEO / Marketing

### Ahrefs Blog Research
**URL:** ahrefs.com/blog — **OPEN**. Big data studies на SEO topics. High quality.

### SEMrush Blog Studies
**URL:** semrush.com/blog/studies — **OPEN**. Similar to Ahrefs.

### Backlinko
**URL:** backlinko.com — **OPEN**. Brian Dean's research-based posts с big data.

### Moz
**URL:** moz.com/blog — **OPEN**. SEO research, ranking factor studies.

### Search engine market share
- StatCounter (`gs.statcounter.com`) — OPEN, real-time browser/search share
- Cloudflare Radar — alternative

---

## Social media stats (creators)

### Social Blade
**URL:** socialblade.com/<platform>/user/<name>
**Access:** OPEN
**What:** YouTube, Twitter, Instagram, TikTok, Twitch creator stats — subs/followers, growth rate
**When:** creator influence analysis, growth tracking
**Quality:** B (public-API derived); Lag: daily updates
**Combine with:** HypeAuditor для deeper analysis

### Twitch Tracker
**URL:** twitchtracker.com — **OPEN**. Twitch-specific deep stats, viewer hours.

### Subreddit Stats
**URL:** subredditstats.com/r/<sub> — **OPEN**. Reddit community growth.

### YouTube Stats Tools
- vidIQ, TubeBuddy — partial open data
- NoxInfluencer — partial

### HypeAuditor
**URL:** hypeauditor.com — **PARTIAL**. Influencer analytics, fake follower detection.

---

## Quick reference

| Что ищем | Источник |
|---|---|
| Mobile app downloads/revenue | Sensor Tower + data.ai (triangulate) |
| Website traffic | SimilarWeb (estimates) + Cloudflare Radar (macro) |
| Site tech stack | BuiltWith + Wappalyzer |
| SaaS reviews | G2 + Capterra (cross-check) |
| Company headcount | LinkedIn (range) + Crunchbase |
| Employee sentiment | Glassdoor |
| YouTube creator stats | Social Blade |
| Twitch creator stats | Twitch Tracker |
| Browser/OS share | StatCounter |
| SEO traffic research | Ahrefs + SEMrush blogs |

## Critical reminders

- Mobile app stats — все estimates (panel-based). ±30% common error.
- SimilarWeb для small sites — низкое качество.
- Self-reported sources (Glassdoor, Indie Hackers) — selection bias.
- Cross-check критические claims через 2-3 источника.

## Combining patterns

**Competitor digital landscape:**
SimilarWeb (traffic) + Crunchbase (funding) + BuiltWith (stack) + LinkedIn (team) + Glassdoor (culture) + G2 (reviews)

**Mobile app market:**
Sensor Tower + data.ai (downloads/revenue triangulate) + AppFigures (charts) + App Store own analysis (если applicable)

**SaaS product validation:**
G2 + Capterra (reviews) + Product Hunt (launch) + Latka/Indie Hackers (если self-reports) + Glassdoor (culture)
