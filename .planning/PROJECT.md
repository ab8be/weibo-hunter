# Weibo Hunter Repair

## What This Is

This is an existing Scrapy-based Weibo search crawler that should fetch posts from `s.weibo.com` for configured keywords, date ranges, content filters, and regions, then persist results to CSV and optional storage backends. The current project goal is to repair and harden the crawler so it can be installed, configured, run, and verified for Weibo search scraping with a valid user cookie.

## Core Value

Given a valid Weibo cookie and search configuration, the crawler can reliably collect Weibo search results and write correct, deduplicated output without crashing.

## Requirements

### Validated

- ✓ Scrapy project structure exists with a registered `search` spider — existing
- ✓ Search URL generation supports keywords, topics, date ranges, Weibo type filters, content filters, and province filters — existing
- ✓ Adaptive subdivision exists for high-volume searches from full range to day, hour, province, and city — existing
- ✓ CSV output pipeline writes Chinese-compatible UTF-8 files under keyword-specific result directories — existing
- ✓ Optional MySQL, MongoDB, SQLite, image, and video pipelines are present but disabled by default — existing
- ✓ Codebase map exists under `.planning/codebase/` — existing

### Active

- [ ] Fresh setup installs all hard runtime dependencies needed to run `scrapy crawl search`.
- [ ] User can configure Weibo cookie without committing secrets to source control.
- [ ] Spider startup validates required settings and reports actionable errors.
- [ ] Spider parsing tolerates missing or changed Weibo HTML elements instead of crashing on common selector failures.
- [ ] Search pagination and adaptive subdivision preserve keyword/province/date context across follow-up requests.
- [ ] IP/region lookup does not block or destabilize the main Scrapy crawl path.
- [ ] Result limit behavior stops at the configured maximum without overshooting or inconsistent counting.
- [ ] Default output remains CSV, with existing item fields preserved.
- [ ] Minimal regression tests cover utility conversion, settings validation, deduplication, and representative parsing helpers.
- [ ] README explains the repaired install, cookie, configuration, and run workflow.

### Out of Scope

- Automated Weibo login or cookie refresh — requires account-specific flows and is not needed to restore cookie-based scraping.
- Circumventing Weibo anti-bot controls — the project should remain a configurable crawler, not an evasion framework.
- Replacing Scrapy with another framework — existing architecture is serviceable and repair scope should stay small.
- A graphical interface — current users operate via settings and Scrapy CLI.
- Large-scale distributed crawling — current goal is local reliability, not horizontal scaling.
- Full database backend redesign — optional backends can be stabilized where touched, but CSV-first scraping is the v1 target.

## Context

The repository is a brownfield Python/Scrapy project. `README.md` describes the intended capability: continuously scrape Weibo keyword search results for one or more keywords over a date range, optionally split dense result sets to avoid Weibo's page cap, and write posts to CSV, databases, images, or videos.

The codebase map identifies several current blockers and risks:

- `requirements.txt` only declares `Pillow>=8.1.1`, but the code imports Scrapy and requests directly.
- `weibo/settings.py` stores a placeholder cookie in source, and README currently instructs users to edit settings directly.
- `SearchSpider` loads settings at class definition time, making startup validation, tests, and runtime overrides brittle.
- `parse_weibo()` assumes many XPath selectors are present and can crash when Weibo changes markup or authentication expires.
- `get_ip()` performs synchronous `requests.get()` calls inside the spider parse path, bypassing Scrapy retry/proxy/timeout behavior and blocking the reactor.
- Debug prints leak noisy output and should move to structured Scrapy logging.
- No tests exist, so repairs need regression coverage before larger cleanup.

## Constraints

- **Tech stack**: Keep Scrapy as the crawler framework because the repository already uses Scrapy spiders, requests, items, and pipelines.
- **Compatibility**: Preserve existing settings names and CSV column layout where practical so existing users do not need to relearn the tool.
- **Authentication**: Assume users provide their own valid Weibo cookie; do not implement automated login.
- **Safety**: Do not commit real cookies, database passwords, or other account secrets.
- **Scope**: Prioritize making Weibo search scraping usable over broad refactoring.
- **Verification**: Add local tests and a dry-run-friendly validation path because live Weibo scraping depends on external credentials and site behavior.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Repair as a brownfield Scrapy project | Existing code already models crawl strategy and output pipeline; replacement would add risk. | — Pending |
| CSV remains the default output | It is documented, enabled by default, and easiest to verify locally. | — Pending |
| Cookie should come from environment or local-only settings | Prevents accidental credential commits while preserving manual cookie workflow. | — Pending |
| Add tests before heavy parser cleanup | Weibo selectors are fragile; tests are needed to keep behavior stable during repairs. | — Pending |
| Keep phase granularity coarse | The repair has a clear path: setup/config, crawler robustness, persistence/docs, verification. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check -> still the right priority?
3. Audit Out of Scope -> reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-26 after initialization*
