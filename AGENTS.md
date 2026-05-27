<!-- GSD:project-start source:PROJECT.md -->
## AI Agent Operating Contract

This repository is intended to be usable by humans and AI coding agents.

Agent-safe collection entry point:

```bash
python scripts/collect_weibo.py --keyword 迪丽热巴 --start-date 2020-03-01 --end-date 2020-03-01 --limit 100
```

Required secret handling:

- Use `WEIBO_COOKIE`; never write real Cookie values into source files.
- Do not commit `结果文件/`, `crawls/`, or other runtime artifacts.
- For orientation, read `docs/AI_AGENT_GUIDE.md` and `docs/COLLECTION_CONTRACT.md`.
- Before claiming collection behavior works, run `python -m pytest -q`, `python -m scrapy list`, and a dry run with `scripts/collect_weibo.py --dry-run`.

## Project

**Weibo Hunter Repair**

This is an existing Scrapy-based Weibo search crawler that should fetch posts from `s.weibo.com` for configured keywords, date ranges, content filters, and regions, then persist results to CSV and optional storage backends. The current project goal is to repair and harden the crawler so it can be installed, configured, run, and verified for Weibo search scraping with a valid user cookie.

**Core Value:** Given a valid Weibo cookie and search configuration, the crawler can reliably collect Weibo search results and write correct, deduplicated output without crashing.

### Constraints

- **Tech stack**: Keep Scrapy as the crawler framework because the repository already uses Scrapy spiders, requests, items, and pipelines.
- **Compatibility**: Preserve existing settings names and CSV column layout where practical so existing users do not need to relearn the tool.
- **Authentication**: Assume users provide their own valid Weibo cookie; do not implement automated login.
- **Safety**: Do not commit real cookies, database passwords, or other account secrets.
- **Scope**: Prioritize making Weibo search scraping usable over broad refactoring.
- **Verification**: Add local tests and a dry-run-friendly validation path because live Weibo scraping depends on external credentials and site behavior.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Core Framework
- **Scrapy** (version not pinned) -- Web scraping framework; provides spider lifecycle, request scheduling, response parsing, item pipelines, and built-in support for file/image downloads.
- Spider class: `SearchSpider` in `weibo/spiders/search.py`, registered name `search`
- Project config: `scrapy.cfg` (standard Scrapy project layout)
## Language and Runtime
- **Python** (version not specified; no `.python-version`, `pyproject.toml`, or `setup.py` present)
- Encoding: `utf-8` throughout; CSV output uses `utf-8-sig` encoding (`weibo/pipelines.py:33`)
- File paths use `os.sep` for cross-platform compatibility (`weibo/pipelines.py:23`)
## Dependencies
### Production
| Package | Version Constraint | Purpose | Where Used |
|---------|--------------------|---------|------------|
| `scrapy` | `>=2.11,<3` | Core scraping framework | All spider/pipeline/middleware files |
| `Pillow` | `>=8.1.1` (in `requirements.txt`) | Image processing for `ImagesPipeline` | `weibo/pipelines.py:130` |
| `requests` | `>=2.31,<3` | Optional Weibo AJAX API call for IP/region lookup when `WEIBO_FETCH_IP=1` | `weibo/spiders/search.py` |
| `pymysql` | Not declared (optional, lazy-imported) | MySQL database driver | `weibo/pipelines.py:209,249` |
| `pymongo` | Not declared (optional, lazy-imported) | MongoDB database driver | `weibo/pipelines.py:179,187` |
| `sqlite3` | stdlib (no install needed) | SQLite database driver | `weibo/pipelines.py:73` |
### Development
- `pytest>=8,<9` is declared for regression tests. No linter or formatter config is currently present.
## Storage Backends
| Backend | Status | Driver | Config Location |
|---------|--------|--------|-----------------|
| CSV | Enabled (default) | stdlib `csv` | `weibo/pipelines.py:21-67` |
| SQLite | Disabled (commented out) | `sqlite3` (stdlib) | `weibo/pipelines.py:69-128` |
| MySQL | Disabled (commented out) | `pymysql` | `weibo/pipelines.py:206-289` |
| MongoDB | Disabled (commented out) | `pymongo` | `weibo/pipelines.py:176-203` |
| Image download | Disabled (commented out) | Scrapy `ImagesPipeline` | `weibo/pipelines.py:130-158` |
| Video download | Disabled (commented out) | Scrapy `FilesPipeline` | `weibo/pipelines.py:161-173` |
## External Services
- **Weibo Search Pages** -- `https://s.weibo.com/weibo?q=...` (HTML scraping via XPath)
- **Weibo AJAX API** -- `https://weibo.com/ajax/statuses/show?id={bid}&locale=zh-CN` (optional JSON endpoint for IP/region info; disabled by default with `WEIBO_FETCH_IP=0`)
## Build and Deployment
- **Run command:** `scrapy crawl search` (from project root)
- **No CI/CD:** No GitHub Actions, Jenkins, or other pipeline configs present
- **No Docker:** No Dockerfile or docker-compose
- **No virtual environment config:** No `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`, or `poetry.lock`
- **Scrapy deploy:** `scrapy.cfg` has a `[deploy]` section for Scrapyd but the URL is commented out (`scrapy.cfg:9-10`)
## Configuration
| Setting | Type | Default | Purpose |
|---------|------|---------|---------|
| `KEYWORD_LIST` | list or filepath | `['迪丽热巴']` | Search keywords; can be inline list or path to `.txt` file |
| `WEIBO_TYPE` | int (0-6) | `1` (original posts) | Weibo type filter |
| `CONTAIN_TYPE` | int (0-4) | `0` (no filter) | Content type filter (images, video, etc.) |
| `REGION` | list | `['全部']` | Province/city region filter |
| `START_DATE` / `END_DATE` | string `yyyy-mm-dd` | `'2020-03-01'` | Date range for search |
| `FURTHER_THRESHOLD` | int | `46` | Page count threshold to trigger date sub-division |
| `LIMIT_RESULT` | int | `0` (unlimited) | Max results before auto-stop |
| `DOWNLOAD_DELAY` | int | `10` | Seconds between requests |
| `LOG_LEVEL` | string | `'ERROR'` | Scrapy log verbosity |
| `COOKIES_ENABLED` | bool | `False` | Scrapy cookie middleware disabled (cookie sent via headers instead) |
| `IMAGES_STORE` / `FILES_STORE` | string | `'./'` | Download paths for images/videos |
| `DEFAULT_REQUEST_HEADERS` | dict | reads `WEIBO_COOKIE` from environment | Request headers with user-supplied cookie |
- `MONGO_URI`: `'localhost'`
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- `SQLITE_DATABASE`: `'weibo.db'`
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Snake_case for all Python files: `search.py`, `pipelines.py`, `region.py`, `util.py`
- `__init__.py` files present in every package directory (empty, no re-exports)
- PascalCase: `SearchSpider`, `WeiboItem`, `CsvPipeline`, `MysqlPipeline`, `DuplicatesPipeline`
- Old-style `(object)` base class on all non-Scrapy classes (Python 2 compatibility holdover)
- Scrapy classes inherit from their framework base: `scrapy.Spider`, `scrapy.Item`, `ImagesPipeline`, `FilesPipeline`
- Snake_case: `convert_weibo_type`, `get_keyword_list`, `standardize_date`, `parse_weibo`, `check_limit`
- Spider callback methods prefixed with `parse`: `parse`, `parse_page`, `parse_by_day`, `parse_by_hour`, `parse_by_hour_province`, `parse_weibo`
- Private helper methods descriptive: `get_article_url`, `get_location`, `get_at_users`, `get_topics`, `get_ip`, `get_vip`
- Snake_case: `keyword_list`, `start_date`, `end_date`, `weibo_type`, `contain_type`, `base_url`, `result_count`
- Boolean error flags: `mongo_error`, `pymongo_error`, `mysql_error`, `pymysql_error`, `sqlite3_error`
- CSS class selectors stored as XPath strings inline, never extracted to constants
- Scrapy settings in UPPER_SNAKE_CASE: `KEYWORD_LIST`, `WEIBO_TYPE`, `CONTAIN_TYPE`, `REGION`, `START_DATE`, `END_DATE`, `FURTHER_THRESHOLD`, `LIMIT_RESULT`, `DOWNLOAD_DELAY`
- No Python-level constants defined; all configuration lives in `weibo/settings.py`
## Code Style
- Every `.py` file begins with `# -*- coding: utf-8 -*-` (line 1)
- Exception: `weibo/utils/util.py` and `weibo/utils/region.py` omit this declaration
- 4-space indentation throughout
- No formatter or linter configured (no `.flake8`, `pyproject.toml`, `setup.cfg`, `ruff.toml`)
- Line lengths are inconsistent; some lines exceed 100 characters (e.g., `search.py:78-80`, `pipelines.py:272-275`)
- Single blank lines between methods, double blank lines between top-level definitions
- No type hints anywhere in the codebase
- No `from __future__ import annotations`
- Mixed approaches: `%` formatting (`'不存在%s文件'`), `.format()` (`'{table}({keys})'`), f-strings (`f'已达到爬取结果数量限制：{self.limit_result}条'`)
- No consistent preference; newer code tends to use f-strings
## Import Organization
- Wildcard imports: none
- Alias usage: `import weibo.utils.util as util` in `weibo/spiders/search.py`
- Imports at module top level, except: `pymysql` and `pymongo` imported inside `open_spider()` methods to allow graceful failure when libraries are missing
- `sqlite3` imported inside `open_spider()` in `SQLitePipeline` following the same pattern
- None; all imports use relative or package-qualified paths
## Language Usage
- Runtime logs are mostly Chinese and use Scrapy logger.
- Error messages are Chinese: `'不存在%s文件'`, `'settings.py配置错误'`
- CSV column headers are Chinese: `'用户昵称'`, `'微博正文'`, `'发布位置'`
- Directory names use Chinese: `'结果文件'` (result files directory)
- Short Chinese docstrings on utility functions: `"""将微博类型转换成字符串"""`, `"""标准化微博发布时间"""`
- Comments are mixed Chinese/English, predominantly Chinese: `# 获取一个省的搜索结果`
- Class names, method names, variable names are all English
- Scrapy boilerplate comments are English (from `scrapy startproject`)
- XPath selectors use English HTML class names from Weibo's DOM
## Error Handling Patterns
- Database pipelines catch exceptions in `open_spider()` and set flags on the spider object.
- Pipeline `process_item()` methods catch exceptions silently in some cases (`MysqlPipeline.process_item` line 281: bare `except Exception` with rollback but no logging)
- `MongoPipeline.close_spider()` catches `AttributeError` silently when client was never initialized
- `check_environment()` reads pipeline error flags and raises `CloseSpider()` with Scrapy logger output.
- Configuration errors are raised as `CloseSpider` during spider startup, not at import time.
- `CloseSpider` is used for runtime stop conditions such as missing Cookie, invalid dates, or result limits.
- No structured error recovery; failures either halt the spider or are swallowed
- `get_keyword_list()` raises `ValueError` for invalid encoding; `SearchSpider` converts that to `CloseSpider`.
- Date range validation happens at spider startup.
## Configuration Conventions
- All configuration in `weibo/settings.py` using Scrapy's settings system
- Spider reads settings through `from_crawler(...).configure(crawler.settings)` so Scrapy `-s` overrides are honored.
- Pipelines also call `get_project_settings()` at module level: `settings = get_project_settings()` in `weibo/pipelines.py` line 18
- Default values provided inline in `settings.get()` calls: `settings.get('FURTHER_THRESHOLD', 46)`
- Cookie is read from the `WEIBO_COOKIE` environment variable in `weibo/settings.py`.
- Environment variable support exists for common collection parameters such as keywords, dates, filters, regions, and limits.
- Pipelines toggled by commenting/uncommenting in `ITEM_PIPELINES` dict in `settings.py` (lines 17-25)
- Priority numbers: `DuplicatesPipeline: 300`, `CsvPipeline: 301`, optional pipelines `302-306`
## Item Data Shape
- 21 fields: `id`, `bid`, `user_id`, `screen_name`, `text`, `article_url`, `location`, `at_users`, `topics`, `reposts_count`, `comments_count`, `attitudes_count`, `created_at`, `source`, `pics`, `video_url`, `retweet_id`, `ip`, `user_authentication`, `vip_type`, `vip_level`
- Spider yields `{'weibo': item, 'keyword': keyword}` dict (not a bare `WeiboItem`)
- Pipelines access data as `item['weibo']` dict, with `.get()` for optional fields
- This wrapping dict is a project convention, not a Scrapy convention
## Anti-Patterns and Technical Debt
- Debug `print(...)` calls were removed; spider status uses Scrapy logger.
- `get_ip()` remains a synchronous optional enrichment path, but it is disabled by default and guarded by timeout/exception handling. Leave it off for normal collection unless IP location is explicitly required.
- `weibo/spiders/search.py` is 639 lines containing all parsing logic
- `parse_weibo()` alone (lines 419-639) is 220 lines with deeply nested conditionals
- Should be decomposed into helper classes or mixins
- Settings values like `WEIBO_TYPE`, `CONTAIN_TYPE` are passed directly to URL construction with no validation
- Invalid values silently produce wrong URLs
- `MysqlPipeline.process_item()` line 281: bare `except Exception` catches everything and rolls back, but does not log or set error flag
- `MongoPipeline.close_spider()` line 203: `except AttributeError: pass`
- `SearchSpider` can be imported and unit-tested without live Weibo access. Tests cover settings injection, parser helpers, basic parsing, and wrapper CLI behavior.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System Overview
```text
```
## Component Responsibilities
| Component | Responsibility | File |
|-----------|----------------|------|
| SearchSpider | Generate requests, parse HTML, yield items | `weibo/spiders/search.py` |
| Settings | All runtime configuration (keywords, dates, DB, pipelines) | `weibo/settings.py` |
| WeiboItem | Data schema for a single weibo post (21 fields) | `weibo/items.py` |
| DuplicatesPipeline | In-memory deduplication by weibo id | `weibo/pipelines.py` |
| CsvPipeline | Write items to CSV under Chinese output directory | `weibo/pipelines.py` |
| MysqlPipeline | Upsert items to MySQL (disabled by default) | `weibo/pipelines.py` |
| MongoPipeline | Upsert items to MongoDB (disabled by default) | `weibo/pipelines.py` |
| SQLitePipeline | Insert/replace items to SQLite (disabled by default) | `weibo/pipelines.py` |
| MyImagesPipeline | Download images to local filesystem | `weibo/pipelines.py` |
| MyVideoPipeline | Download videos to local filesystem | `weibo/pipelines.py` |
| util functions | Date normalization, keyword loading, type conversion | `weibo/utils/util.py` |
| region_dict | Province-to-city-code mapping for Weibo region filter API | `weibo/utils/region.py` |
## Pattern Overview
- Cookie-based authentication injected via `DEFAULT_REQUEST_HEADERS` in `settings.py` (no OAuth, no login automation)
- Adaptive subdivision: when a search result page count meets `FURTHER_THRESHOLD`, the spider narrows the time window (full range -> day -> hour -> city) to bypass Weibo's result cap
- Direct `requests.get()` call in `SearchSpider.get_ip()` (`weibo/spiders/search.py:322-333`) bypasses Scrapy's request pipeline, downloader middleware, and retry logic
- Retweet handling: both the retweeted original and the retweeting post are yielded as separate items (`weibo/spiders/search.py:605, 635`)
## Spider Parsing Hierarchy
## Data Flow
### Primary Request Path
### Retweet Handling Flow
### IP Lookup Flow
- Spider settings are loaded from Scrapy runtime settings so `-s` command-line overrides are honored.
- Instance variables (`self.result_count`) track runtime progress
- Error flags (`self.mongo_error`, `self.mysql_error`, etc.) are set by pipelines and checked by `check_environment()`
- `DuplicatesPipeline` uses an in-memory `set()` (`self.ids_seen`) -- not persistent across runs
## Error Handling
- Pipelines catch exceptions and set flags: `spider.mongo_error = True` (`weibo/pipelines.py:197`)
- `SearchSpider.check_environment()` (`weibo/spiders/search.py:93-110`) raises `CloseSpider` if any flag is set
- `check_environment()` is called in every parse method before yielding items
- If `LIMIT_RESULT` is set, `check_limit()` raises `CloseSpider` when `self.result_count` exceeds limit (`weibo/spiders/search.py:50-55`)
## Data Model
| Field | Type | Description |
|-------|------|-------------|
| id | str | Weibo's internal numeric ID (mid) |
| bid | str | Short ID from URL path |
| user_id | str | Author's numeric user ID |
| screen_name | str | Author's display name |
| text | str | Post body text (HTML-stripped) |
| article_url | str | URL if post is a "headline article" |
| location | str | Posted location (if tagged) |
| at_users | str | Comma-separated mentioned users |
| topics | str | Comma-separated hashtags (without #) |
| reposts_count | str | Number of reposts |
| comments_count | str | Number of comments |
| attitudes_count | str | Number of likes |
| created_at | str | Normalized datetime string "YYYY-MM-DD HH:MM" |
| source | str | Client used to post (e.g., "iPhone客户端") |
| pics | list/str | List of image URLs (or empty string for retweets) |
| video_url | str | Video URL if present |
| retweet_id | str | ID of the retweeted weibo (empty if original) |
| ip | str | Region name from API (e.g., "北京") |
| user_authentication | str | Verification type: "蓝V"/"黄V"/"红V"/"金V"/"普通用户" |
| vip_type | str | VIP type: "超级会员"/"会员"/"非会员" |
| vip_level | int | VIP level (0-9) |
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
