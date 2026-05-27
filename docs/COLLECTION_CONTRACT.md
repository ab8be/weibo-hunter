# Collection Contract

This document defines the stable interface for humans, IDEs, Claude Code, Codex, Cursor, and other AI agents that need to collect Weibo search data with this repository.

## Inputs

Required:

- `cookie`: provided through `WEIBO_COOKIE`.
- `keywords`: one or more search terms.
- `start_date`: `yyyy-mm-dd`.
- `end_date`: `yyyy-mm-dd`.

Recommended:

- `limit`: positive integer for bounded runs.
- `download_delay`: seconds between requests.

Optional:

- `weibo_type`: `0` all, `1` original, `2` hot, `3` following, `4` verified, `5` media, `6` viewpoint.
- `contain_type`: `0` all, `1` image, `2` video, `3` music, `4` link.
- `region`: province/municipality names supported by `weibo/utils/region.py`, or `全部`.
- `jobdir`: Scrapy resume directory.

## Preferred CLI

```bash
python scripts/collect_weibo.py --keyword <keyword> --start-date <yyyy-mm-dd> --end-date <yyyy-mm-dd> --limit <n>
```

Multiple keywords:

```bash
python scripts/collect_weibo.py --keyword 迪丽热巴 --keyword 杨幂 --start-date 2020-03-01 --end-date 2020-03-01 --limit 100
```

Dry run:

```bash
python scripts/collect_weibo.py --keyword 迪丽热巴 --start-date 2020-03-01 --end-date 2020-03-01 --limit 5 --dry-run
```

Dry-run output intentionally reports whether a cookie is present but never prints the cookie value.

## Direct Scrapy CLI

Direct Scrapy usage remains supported:

```bash
python -m scrapy crawl search -s LIMIT_RESULT=100 -s DOWNLOAD_DELAY=1
```

When using direct Scrapy, configure search scope through environment variables or `weibo/settings.py`.

## Outputs

Default output:

```text
结果文件/<keyword>/<keyword>.csv
```

Encoding:

```text
utf-8-sig
```

Each item yielded to pipelines has this shape:

```python
{
    "keyword": "迪丽热巴",
    "weibo": {
        "id": "...",
        "bid": "...",
        "user_id": "...",
        "screen_name": "...",
        "text": "...",
        "article_url": "",
        "location": "",
        "at_users": "",
        "topics": "",
        "reposts_count": "0",
        "comments_count": "0",
        "attitudes_count": "0",
        "created_at": "2020-03-01 16:59",
        "source": "",
        "pics": [],
        "video_url": "",
        "retweet_id": "",
        "ip": "",
        "user_authentication": "普通用户",
        "vip_type": "非会员",
        "vip_level": 0
    }
}
```

## Success Criteria

A collection run is successful when:

- The process exits `0`.
- Scrapy opens the `search` spider.
- The run either scrapes at least one item or logs that the Weibo result page is empty.
- CSV output is created or appended for non-empty results.
- No cookie value appears in committed files, logs intended for sharing, or documentation.

## Verification Commands

```bash
python -m scrapy list
python -m pytest -q
python scripts/collect_weibo.py --keyword 测试 --start-date 2020-01-01 --end-date 2020-01-01 --limit 5 --dry-run
```
