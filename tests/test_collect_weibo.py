import json

import pytest

from scripts import collect_weibo


def parse_args(args):
    return collect_weibo.build_parser().parse_args(args)


def test_collect_weibo_requires_keyword():
    args = parse_args(['--start-date', '2020-01-01', '--end-date', '2020-01-01'])

    with pytest.raises(SystemExit, match='At least one'):
        collect_weibo.read_keywords(args)


def test_collect_weibo_builds_safe_env_without_printing_cookie(monkeypatch):
    monkeypatch.setenv('WEIBO_COOKIE', 'secret-cookie')
    args = parse_args([
        '--keyword', '迪丽热巴',
        '--keyword', '杨幂',
        '--start-date', '2020-01-01',
        '--end-date', '2020-01-02',
        '--limit', '7',
        '--region', '北京',
    ])

    env = collect_weibo.build_env(args, collect_weibo.read_keywords(args))

    assert env['WEIBO_COOKIE'] == 'secret-cookie'
    assert json.loads(env['WEIBO_KEYWORDS']) == ['迪丽热巴', '杨幂']
    assert env['WEIBO_START_DATE'] == '2020-01-01'
    assert env['WEIBO_END_DATE'] == '2020-01-02'
    assert env['WEIBO_LIMIT_RESULT'] == '7'
    assert json.loads(env['WEIBO_REGION']) == ['北京']


def test_collect_weibo_dry_run_hides_cookie(monkeypatch, capsys):
    monkeypatch.setenv('WEIBO_COOKIE', 'secret-cookie')

    exit_code = collect_weibo.main([
        '--keyword', '测试',
        '--start-date', '2020-01-01',
        '--end-date', '2020-01-01',
        '--limit', '5',
        '--dry-run',
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert 'COOKIE_PRESENT=true' in output
    assert 'secret-cookie' not in output
    assert 'WEIBO_KEYWORDS' in output
