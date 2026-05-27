# AI Agent Guide

This project is a Scrapy crawler for collecting Weibo search results from `s.weibo.com`.

## Mission

Given a valid Weibo Cookie and a bounded search plan, collect Weibo posts for keywords and dates, then write CSV output under `结果文件/<keyword>/<keyword>.csv`.

## Safe Defaults

- Never write real cookies into source files.
- Use `WEIBO_COOKIE` for authentication.
- Start every live run with `--limit` or `WEIBO_LIMIT_RESULT`.
- Prefer CSV output unless the user explicitly asks for a database pipeline.
- Treat `结果文件/` and `crawls/` as runtime artifacts, not source.

## Fast Orientation

| Need | File |
|------|------|
| Spider request/parse logic | `weibo/spiders/search.py` |
| Runtime settings | `weibo/settings.py` |
| CSV/database/media pipelines | `weibo/pipelines.py` |
| Item schema | `weibo/items.py` |
| Region mapping | `weibo/utils/region.py` |
| Human docs | `README.md` |
| Repair and verification summary | `docs/REPAIR_REPORT.md` |
| Machine-readable collection contract | `docs/COLLECTION_CONTRACT.md` |
| Agent-friendly run wrapper | `scripts/collect_weibo.py` |

## Standard Commands

Validate without live Weibo access:

```bash
python -m scrapy list
python -m pytest -q
python scripts/collect_weibo.py --keyword 测试 --start-date 2020-01-01 --end-date 2020-01-01 --limit 5 --dry-run
```

Run a bounded live collection:

```bash
python scripts/collect_weibo.py --keyword 迪丽热巴 --start-date 2020-03-01 --end-date 2020-03-01 --limit 100
```

PowerShell setup:

```powershell
$env:WEIBO_COOKIE = "real cookie"
python scripts/collect_weibo.py --keyword 迪丽热巴 --start-date 2020-03-01 --end-date 2020-03-01 --limit 100
```

## Environment Interface

The crawler supports these environment variables:

| Variable | Meaning | Example |
|----------|---------|---------|
| `WEIBO_COOKIE` | Required login Cookie | Browser Cookie string |
| `WEIBO_KEYWORDS` | JSON list or comma-separated keywords | `["迪丽热巴","杨幂"]` |
| `WEIBO_START_DATE` | Inclusive start date | `2020-03-01` |
| `WEIBO_END_DATE` | Inclusive end date | `2020-03-02` |
| `WEIBO_LIMIT_RESULT` | Max items, `0` means unlimited | `100` |
| `WEIBO_TYPE` | Search type, see README | `1` |
| `WEIBO_CONTAIN_TYPE` | Content filter, see README | `0` |
| `WEIBO_REGION` | JSON list or comma-separated regions | `["全部"]` |
| `WEIBO_FETCH_IP` | Optional IP enrichment flag | `0` or `1` |

Scrapy `-s` overrides still work for settings such as `LIMIT_RESULT`, `DOWNLOAD_DELAY`, `LOG_LEVEL`, and `JOBDIR`.

## Output Contract

Default CSV columns are stable and documented in `README.md`. AI consumers should read CSV with `utf-8-sig` encoding.

Minimum success evidence for a live run:

- Command exits with code `0`.
- Scrapy stats include `item_scraped_count > 0`, or the log clearly says the result page was empty.
- Expected CSV file exists under `结果文件/<keyword>/<keyword>.csv`.
- The run used a bounded `limit` unless the user explicitly requested unlimited collection.

## Common Failure Modes

- Missing Cookie: set `WEIBO_COOKIE`.
- Expired Cookie: refresh Cookie from browser and retry.
- Empty result: check keyword/date/type/region filters.
- Layout drift: update selectors in `weibo/spiders/search.py` and add parser tests.
- Too many rows: set `--limit` or `WEIBO_LIMIT_RESULT`.

## Change Rules For Agents

- Do not commit cookies, generated CSVs, or `crawls/`.
- Add or update tests when changing parsing, settings, or pipelines.
- Run `python -m pytest -q` and `python -m scrapy list` before reporting completion.
- If touching live collection behavior, run `scripts/collect_weibo.py --dry-run` at minimum.
