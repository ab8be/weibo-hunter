"""Agent-friendly CLI wrapper for running the Weibo search spider."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run a bounded Weibo search collection with env-based settings.'
    )
    parser.add_argument('--keyword', action='append', dest='keywords',
                        help='Keyword to search. Repeat for multiple keywords.')
    parser.add_argument('--keywords-file',
                        help='UTF-8 text file with one keyword per line.')
    parser.add_argument('--start-date', required=True,
                        help='Inclusive start date, yyyy-mm-dd.')
    parser.add_argument('--end-date', required=True,
                        help='Inclusive end date, yyyy-mm-dd.')
    parser.add_argument('--limit', type=int, default=20,
                        help='Maximum result items to scrape. Use 0 for unlimited.')
    parser.add_argument('--weibo-type', type=int, default=1,
                        help='0 all, 1 original, 2 hot, 3 following, 4 verified, 5 media, 6 viewpoint.')
    parser.add_argument('--contain-type', type=int, default=0,
                        help='0 all, 1 image, 2 video, 3 music, 4 link.')
    parser.add_argument('--region', action='append', default=None,
                        help='Province/municipality filter. Repeat for multiple regions. Default: 全部.')
    parser.add_argument('--download-delay', type=float, default=1.0,
                        help='Seconds between requests.')
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--jobdir', default=None,
                        help='Optional Scrapy JOBDIR for resumable crawls.')
    parser.add_argument('--cookie-env', default='WEIBO_COOKIE',
                        help='Environment variable containing the Weibo Cookie.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print the command and derived environment without crawling.')
    return parser


def read_keywords(args: argparse.Namespace) -> list[str]:
    keywords = list(args.keywords or [])
    if args.keywords_file:
        path = Path(args.keywords_file)
        keywords.extend(
            line.strip() for line in path.read_text(encoding='utf-8-sig').splitlines()
            if line.strip())
    if not keywords:
        raise SystemExit('At least one --keyword or --keywords-file is required.')
    return keywords


def build_env(args: argparse.Namespace, keywords: list[str]) -> dict[str, str]:
    cookie = os.getenv(args.cookie_env, '').strip()
    if not cookie:
        raise SystemExit(f'{args.cookie_env} is empty. Set it to a valid Weibo Cookie first.')
    env = os.environ.copy()
    env['WEIBO_COOKIE'] = cookie
    env['WEIBO_KEYWORDS'] = json.dumps(keywords, ensure_ascii=False)
    env['WEIBO_START_DATE'] = args.start_date
    env['WEIBO_END_DATE'] = args.end_date
    env['WEIBO_TYPE'] = str(args.weibo_type)
    env['WEIBO_CONTAIN_TYPE'] = str(args.contain_type)
    env['WEIBO_REGION'] = json.dumps(args.region or ['全部'], ensure_ascii=False)
    env['WEIBO_LIMIT_RESULT'] = str(args.limit)
    return env


def build_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        '-m',
        'scrapy',
        'crawl',
        'search',
        '-s',
        f'LIMIT_RESULT={args.limit}',
        '-s',
        f'DOWNLOAD_DELAY={args.download_delay}',
        '-s',
        f'LOG_LEVEL={args.log_level}',
    ]
    if args.jobdir:
        command.extend(['-s', f'JOBDIR={args.jobdir}'])
    return command


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    keywords = read_keywords(args)
    env = build_env(args, keywords)
    command = build_command(args)
    if args.dry_run:
        safe_env = {
            key: env[key]
            for key in [
                'WEIBO_KEYWORDS',
                'WEIBO_START_DATE',
                'WEIBO_END_DATE',
                'WEIBO_TYPE',
                'WEIBO_CONTAIN_TYPE',
                'WEIBO_REGION',
                'WEIBO_LIMIT_RESULT',
            ]
        }
        print('COMMAND=' + ' '.join(command))
        print('ENV=' + json.dumps(safe_env, ensure_ascii=False, sort_keys=True))
        print('COOKIE_PRESENT=true')
        return 0
    return subprocess.run(command, env=env, check=False).returncode


if __name__ == '__main__':
    raise SystemExit(main())
