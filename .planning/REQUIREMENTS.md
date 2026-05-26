# Requirements: Weibo Hunter Repair

**Defined:** 2026-05-26
**Core Value:** Given a valid Weibo cookie and search configuration, the crawler can reliably collect Weibo search results and write correct, deduplicated output without crashing.

## v1 Requirements

### Setup

- [ ] **SETUP-01**: User can install all runtime dependencies from `requirements.txt` in a fresh Python environment.
- [ ] **SETUP-02**: User can run a local validation command that imports the Scrapy project without missing dependency errors.
- [ ] **SETUP-03**: User can configure a Weibo cookie without storing the real cookie in committed source files.

### Configuration

- [ ] **CONF-01**: User receives a clear error when required settings such as keyword list, date range, or cookie are invalid.
- [ ] **CONF-02**: User can continue using existing setting names for keywords, date range, filters, region, threshold, result limit, and output pipelines.
- [ ] **CONF-03**: User can safely use default settings for a small CSV scrape after adding a valid cookie and keyword.

### Crawling

- [ ] **CRAWL-01**: User can start the `search` spider with `scrapy crawl search` and generate Weibo search requests for configured keywords and dates.
- [ ] **CRAWL-02**: Spider preserves keyword, date, province, and city context while following pagination and adaptive subdivision requests.
- [ ] **CRAWL-03**: Spider handles empty result pages, expired-cookie pages, and missing expected selectors with actionable logs instead of unhandled exceptions.
- [ ] **CRAWL-04**: Spider respects `LIMIT_RESULT` and stops cleanly when the configured result count is reached.
- [ ] **CRAWL-05**: Optional IP/region enrichment does not block the Scrapy reactor or crash the crawl when the AJAX endpoint fails.

### Parsing

- [ ] **PARSE-01**: User receives parsed post fields for normal search results, including id, bid, user id, screen name, text, created time, counts, source, media, topics, mentions, verification, VIP, and location fields where available.
- [ ] **PARSE-02**: User receives both retweet and main post records when a search result contains a retweet, preserving `retweet_id` linkage.
- [ ] **PARSE-03**: Parser tolerates absent optional fields such as source, media, article URL, location, VIP icons, and verification icons.

### Output

- [ ] **OUT-01**: User can write deduplicated results to CSV with the existing column order and UTF-8 BOM encoding.
- [ ] **OUT-02**: User can enable optional SQLite output without crashing on normal item fields.
- [ ] **OUT-03**: Pipeline errors are logged clearly and stop or skip work consistently instead of failing silently.

### Verification

- [ ] **TEST-01**: Maintainer can run automated tests for utility conversions, keyword loading, region filtering, deduplication, configuration validation, and parser helper behavior.
- [ ] **TEST-02**: Maintainer can verify spider import/startup without contacting Weibo.
- [ ] **TEST-03**: README documents manual live verification steps requiring a valid Weibo cookie.

## v2 Requirements

### Performance

- **PERF-01**: Spider supports cached or asynchronous IP enrichment for large crawls.
- **PERF-02**: Deduplication can persist across resumed runs.
- **PERF-03**: Crawl rate limits and concurrency settings can be tuned per run without editing source.

### Maintainability

- **MAINT-01**: `parse_weibo()` is split into smaller parser components with focused tests.
- **MAINT-02**: MySQL and MongoDB pipelines are hardened with explicit optional dependencies and safer query construction.
- **MAINT-03**: Logging replaces remaining direct `print()` statements across spider and pipelines.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automated Weibo login | Account-specific and not required for restoring cookie-based search scraping. |
| CAPTCHA or anti-bot bypass | Outside repair scope and likely unstable. |
| Distributed crawler orchestration | Local Scrapy reliability is the current goal. |
| GUI configuration app | CLI/settings workflow is already documented and sufficient for v1. |
| Full database backend redesign | CSV output is the default v1 success path; optional databases can be improved later. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SETUP-01 | Phase 1 | Pending |
| SETUP-02 | Phase 1 | Pending |
| SETUP-03 | Phase 1 | Pending |
| CONF-01 | Phase 1 | Pending |
| CONF-02 | Phase 1 | Pending |
| CONF-03 | Phase 1 | Pending |
| CRAWL-01 | Phase 2 | Pending |
| CRAWL-02 | Phase 2 | Pending |
| CRAWL-03 | Phase 2 | Pending |
| CRAWL-04 | Phase 2 | Pending |
| CRAWL-05 | Phase 2 | Pending |
| PARSE-01 | Phase 2 | Pending |
| PARSE-02 | Phase 2 | Pending |
| PARSE-03 | Phase 2 | Pending |
| OUT-01 | Phase 3 | Pending |
| OUT-02 | Phase 3 | Pending |
| OUT-03 | Phase 3 | Pending |
| TEST-01 | Phase 4 | Pending |
| TEST-02 | Phase 4 | Pending |
| TEST-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-05-26*
*Last updated: 2026-05-26 after roadmap creation*
