# Roadmap: Weibo Hunter Repair

**Created:** 2026-05-26
**Granularity:** Coarse
**Mode:** YOLO

## Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Setup and Safe Configuration | Make the project installable and safe to configure without committing secrets. | SETUP-01, SETUP-02, SETUP-03, CONF-01, CONF-02, CONF-03 | 4 |
| 2 | Crawl and Parse Robustness | Make Weibo search crawling resilient to common selector, pagination, auth, and enrichment failures. | CRAWL-01, CRAWL-02, CRAWL-03, CRAWL-04, CRAWL-05, PARSE-01, PARSE-02, PARSE-03 | 5 |
| 3 | Output Pipeline Reliability | Preserve CSV output and stabilize optional SQLite/pipeline failure behavior. | OUT-01, OUT-02, OUT-03 | 3 |
| 4 | Verification and Operator Docs | Add regression tests and document the repaired workflow, including live verification. | TEST-01, TEST-02, TEST-03 | 4 |

## Phase Details

### Phase 1: Setup and Safe Configuration

**Goal:** Make the project installable and safe to configure without committing secrets.

**Requirements:** SETUP-01, SETUP-02, SETUP-03, CONF-01, CONF-02, CONF-03

**Success criteria:**
1. A fresh environment can install declared dependencies required by imports used in the project.
2. The spider can be imported or listed by Scrapy without `ModuleNotFoundError`.
3. Real Weibo cookies are loaded from environment or local-only override, while committed defaults remain placeholders.
4. Invalid dates, missing keywords, or missing cookie produce clear startup errors.

**UI hint:** no

### Phase 2: Crawl and Parse Robustness

**Goal:** Make Weibo search crawling resilient to common selector, pagination, auth, and enrichment failures.

**Requirements:** CRAWL-01, CRAWL-02, CRAWL-03, CRAWL-04, CRAWL-05, PARSE-01, PARSE-02, PARSE-03

**Success criteria:**
1. `scrapy crawl search` produces expected request URLs for keyword/date/filter/region combinations.
2. Pagination and subdivision callbacks preserve enough metadata to continue writing results under the correct keyword.
3. Expired-cookie or changed-layout pages produce actionable logs and stop or skip cleanly, not raw `AttributeError` or `IndexError`.
4. Normal, media, topic, mention, VIP, verification, and retweet fields are parsed when present and defaulted when absent.
5. IP enrichment failures do not block or crash main item extraction.

**UI hint:** no

### Phase 3: Output Pipeline Reliability

**Goal:** Preserve CSV output and stabilize optional SQLite/pipeline failure behavior.

**Requirements:** OUT-01, OUT-02, OUT-03

**Success criteria:**
1. CSV output keeps existing header order and writes one row per deduplicated item.
2. The CSV pipeline handles empty optional fields and both string/list `pics` representations.
3. SQLite output can be enabled for standard scraped items without schema/key errors.

**UI hint:** no

### Phase 4: Verification and Operator Docs

**Goal:** Add regression tests and document the repaired workflow, including live verification.

**Requirements:** TEST-01, TEST-02, TEST-03

**Success criteria:**
1. Automated tests cover utility conversions, keyword file loading, region selection, deduplication, validation, and parser helpers.
2. A no-network verification path proves the Scrapy project imports and startup validation works.
3. README documents install, cookie setup, search configuration, CSV output location, and manual live scrape verification.
4. The final verification report identifies any checks that require a real Weibo cookie.

**UI hint:** no

## Coverage Validation

Every v1 requirement in `.planning/REQUIREMENTS.md` maps to exactly one phase.

| Phase | Requirement Count |
|-------|-------------------|
| Phase 1 | 6 |
| Phase 2 | 8 |
| Phase 3 | 3 |
| Phase 4 | 3 |

**Total mapped:** 20
**Unmapped:** 0

---
*Roadmap created: 2026-05-26*
