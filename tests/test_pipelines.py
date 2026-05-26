import csv
from types import SimpleNamespace

import pytest
from scrapy.exceptions import DropItem

from weibo.pipelines import CsvPipeline, DuplicatesPipeline, normalize_pics


def make_item(weibo_id='1', pics=None):
    return {
        'keyword': '测试',
        'weibo': {
            'id': weibo_id,
            'bid': 'abc',
            'user_id': '42',
            'screen_name': '用户',
            'text': '正文',
            'article_url': '',
            'location': '',
            'at_users': '',
            'topics': '',
            'reposts_count': '0',
            'comments_count': '0',
            'attitudes_count': '0',
            'created_at': '2026-05-26 10:00',
            'source': '',
            'pics': [] if pics is None else pics,
            'video_url': '',
            'retweet_id': '',
            'ip': '',
            'user_authentication': '普通用户',
            'vip_type': '非会员',
            'vip_level': 0,
        },
    }


def test_normalize_pics_accepts_list_string_and_empty():
    assert normalize_pics(['https://a', 'https://b']) == 'https://a,https://b'
    assert normalize_pics('https://a') == 'https://a'
    assert normalize_pics([]) == ''
    assert normalize_pics('') == ''


def test_duplicates_pipeline_drops_duplicate_ids():
    pipeline = DuplicatesPipeline()
    spider = SimpleNamespace()

    assert pipeline.process_item(make_item('1'), spider)['weibo']['id'] == '1'
    with pytest.raises(DropItem):
        pipeline.process_item(make_item('1'), spider)


def test_csv_pipeline_writes_header_and_row(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pipeline = CsvPipeline()

    pipeline.process_item(make_item(pics=['https://img']), SimpleNamespace())

    output = tmp_path / '结果文件' / '测试' / '测试.csv'
    rows = list(csv.reader(output.open(encoding='utf-8-sig')))
    assert rows[0][0:4] == ['id', 'bid', 'user_id', '用户昵称']
    assert rows[1][0:4] == ['1', 'abc', '42', '用户']
    assert rows[1][14] == 'https://img'
