import pytest

from weibo.utils import util


def test_convert_weibo_type_defaults_to_original():
    assert util.convert_weibo_type(0) == '&typeall=1'
    assert util.convert_weibo_type(1) == '&scope=ori'
    assert util.convert_weibo_type(99) == '&scope=ori'


def test_convert_contain_type_defaults_to_all():
    assert util.convert_contain_type(0) == '&suball=1'
    assert util.convert_contain_type(2) == '&hasvideo=1'
    assert util.convert_contain_type(99) == '&suball=1'


def test_get_keyword_list_reads_utf8_sig(tmp_path):
    keyword_file = tmp_path / 'keywords.txt'
    keyword_file.write_text('\ufeff迪丽热巴\n\n杨幂\n', encoding='utf-8')

    assert util.get_keyword_list(str(keyword_file)) == ['迪丽热巴', '杨幂']


def test_get_keyword_list_rejects_non_utf8(tmp_path):
    keyword_file = tmp_path / 'keywords.txt'
    keyword_file.write_bytes('测试'.encode('gbk'))

    with pytest.raises(ValueError, match='utf-8'):
        util.get_keyword_list(str(keyword_file))


def test_get_regions_filters_valid_names():
    regions = util.get_regions(['北京'])

    assert list(regions.keys()) == ['北京']


def test_get_regions_defaults_to_all_for_invalid_names():
    regions = util.get_regions(['不存在'])

    assert '北京' in regions
    assert '上海' in regions


def test_standardize_date_handles_relative_time():
    # 相对时间格式应正常标准化，不抛异常。
    result = util.standardize_date('今天 10:00')
    assert result.endswith('10:00')


def test_standardize_date_tolerates_non_numeric_relative_time():
    # 微博偶发的无数字相对时间（验证页残留等），不应抛 ValueError 中断采集。
    assert util.standardize_date('秒前') == '秒前'
    assert util.standardize_date('分钟前') == '分钟前'
