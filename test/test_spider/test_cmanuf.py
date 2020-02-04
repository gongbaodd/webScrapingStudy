from dev.spiders.cmanuf import Cmanuf
from unittest import mock

def test_parseBook():
    spider = Cmanuf()
    response = mock.MagicMock()

    response.meta = {
        'detail': {
            'xxx': 'xxx',
        }
    }
    response.url = 'url'

    item = next(spider.parseBook(response))

    assert(item)
    assert(item['bookUrl'] == 'url')


def test_parse():
    spider = Cmanuf()
    response = mock.MagicMock()
    response.body_as_unicode = mock.MagicMock(
        return_value = '''
        {
            "success": true,
            "module": [
                {
                    "id": "id"
                }
            ]
        }
        '''
    )

    request = next(spider.parse(response))

    assert(request)
    assert(request.url == 'http://ebooks.cmanuf.com/detail?id=id')


def test_getPageIndex():
    spider = Cmanuf()
    code = 'code'
    page = 1

    result = spider.getPageIndex(code, page)
    
    assert(result.url == spider.getBookCategoryInfo)
