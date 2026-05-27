import pytest
from scrapy.exceptions import CloseSpider
from scrapy.settings import Settings
from scrapy.http import HtmlResponse

from weibo.spiders.search import SearchSpider


def response_from_html(html, meta=None):
    request = None
    if meta is not None:
        from scrapy.http import Request

        request = Request('https://s.weibo.com/weibo?q=test', meta=meta)
    return HtmlResponse(
        url='https://s.weibo.com/weibo?q=test',
        body=html.encode('utf-8'),
        encoding='utf-8',
        request=request,
    )


def test_load_keyword_list_encodes_topic():
    spider = SearchSpider()

    assert spider.load_keyword_list(['#话题#', '普通']) == ['%23话题%23', '普通']


def test_constructor_accepts_runtime_settings_override():
    spider = SearchSpider(
        settings=Settings({
            'KEYWORD_LIST': ['测试'],
            'WEIBO_TYPE': 0,
            'CONTAIN_TYPE': 2,
            'REGION': ['全部'],
            'START_DATE': '2020-01-01',
            'END_DATE': '2020-01-01',
            'LIMIT_RESULT': 5,
            'DEFAULT_REQUEST_HEADERS': {
                'cookie': 'dummy'
            },
        }))

    assert spider.limit_result == 5
    assert spider.weibo_type == '&typeall=1'
    assert spider.contain_type == '&hasvideo=1'


def test_load_keyword_list_reports_invalid_encoding(tmp_path):
    keyword_file = tmp_path / 'keywords.txt'
    keyword_file.write_bytes('测试'.encode('gbk'))
    spider = SearchSpider()

    with pytest.raises(CloseSpider) as exc_info:
        spider.load_keyword_list(str(keyword_file))
    assert 'utf-8' in exc_info.value.reason


def test_validate_runtime_settings_requires_cookie():
    spider = SearchSpider()
    spider.project_settings.set('DEFAULT_REQUEST_HEADERS', {'cookie': ''})

    with pytest.raises(CloseSpider) as exc_info:
        spider.validate_runtime_settings()
    assert '未配置微博Cookie' in exc_info.value.reason


def test_get_ip_disabled_by_default():
    spider = SearchSpider()
    spider.fetch_ip = False

    assert spider.get_ip('abc') == ''


def test_parse_weibo_skips_card_missing_core_fields():
    spider = SearchSpider()
    html = '<div class="card-wrap" mid="1"><div class="card"></div></div>'
    response = response_from_html(html, {'keyword': '测试'})

    assert list(spider.parse_weibo(response)) == []


def test_parse_weibo_extracts_basic_card():
    spider = SearchSpider()
    html = '''
    <div class="card-wrap" mid="123">
      <div class="card">
        <div class="card-feed">
          <div class="avator"><svg id="woo_svg_vblue"></svg></div>
          <div class="content">
            <div class="info"><div></div><div><a href="/u/42?x=1" nick-name="用户"></a></div></div>
            <p class="txt">xx正文 #话题# <a href="/n/name">@name</a></p>
            <div class="from"><a href="/42/AbCd?x=1">2026-05-26 10:00</a><a>来源</a></div>
            <a action-type="feed_list_forward">转发 3</a>
            <a action-type="feed_list_comment">评论 4</a>
            <a action-type="feed_list_like"><button><span></span><span>5</span></button></a>
          </div>
        </div>
      </div>
    </div>
    '''
    response = response_from_html(html, {'keyword': '测试'})

    items = list(spider.parse_weibo(response))

    assert len(items) == 1
    weibo = items[0]['weibo']
    assert weibo['id'] == '123'
    assert weibo['bid'] == 'AbCd'
    assert weibo['user_id'] == '42'
    assert weibo['screen_name'] == '用户'
    assert weibo['text'].startswith('正文')
    assert weibo['reposts_count'] == '3'
    assert weibo['comments_count'] == '4'
    assert weibo['attitudes_count'] == '5'
    assert weibo['user_authentication'] == '蓝V'
