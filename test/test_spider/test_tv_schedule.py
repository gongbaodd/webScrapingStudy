from dev.spiders.tv_schedule import TvScheduleSpider
from bs4 import BeautifulSoup
from unittest import mock
import pytest
import logging
import feedparser


def test_tv_schedule_parse_day():
    spider = TvScheduleSpider()
    test_html = '''
    <a href="rss/url/0">link_text_0_1</a>
    <a href="rss/url/0">link_text_0_2</a>
    <a href="rss/url/1">link_text_1_1</a>
    '''
    test_soup = BeautifulSoup(test_html, 'lxml')
    result = spider.parse_day(test_soup)

    assert(result)

    assert(result['0']['episodes'][0] == 'link_text_0_1')
    assert(result['0']['episodes'][1] == 'link_text_0_2')
    assert(result['0']['rss'] == 'http://rss.rrys.tv/rss/feed/0')

    assert(result['1']['episodes'][0] == 'link_text_1_1')
    assert(result['1']['rss'] == 'http://rss.rrys.tv/rss/feed/1')


def test_tv_schedule_parse_days():
    spider = TvScheduleSpider()
    test_html = ['''
        <td>
            <dl>
                <dt>title</dt>
                <dd><a href="rss/0">item</a></dd>
            </dl>
        </td>
    ''']
    days = spider.parse_days(test_html)

    assert(days)
    assert('title' in days)


@mock.patch('feedparser.parse')
def test_tv_schedule_parse_detail(mock_parse):
    spider = TvScheduleSpider()
    next(spider.parse_detail(mock.Mock()))

    assert(mock_parse.called)


def test_tv_schedule_parse():
    spider = TvScheduleSpider()
    spider.parse_days = mock.MagicMock(
        return_value={
            '0': {
                '123': {}
            }
        }
    )
    item = next(spider.parse(mock.Mock()))

    assert(item)


def test_tv_schedule_follow_rss():
    spider = TvScheduleSpider()
    mockResponse = mock.MagicMock()
    mockResponse.follow = mock.MagicMock(return_value='rss')

    result = next(spider.follow_rss(
        {
            'days': {
                '0': {
                    '123': {
                        'rss': '/rss'
                    }
                }
            }
        }, 
        mockResponse
        )
    )

    assert(result == 'rss')

