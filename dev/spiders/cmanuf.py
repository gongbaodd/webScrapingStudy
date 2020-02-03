import scrapy
import json
from scrapy_splash import SplashRequest


class Cmanuf(scrapy.Spider):
    name = 'cmanuf'
    getBookCategoryInfo = 'http://ebooks.cmanuf.com/getBookCategoryInfo'
    bookDetailPrefix = 'http://ebooks.cmanuf.com/detail?id='

    def start_requests(self):
        for index in range(1, 24):
            if index/10 < 1:
                code = 'AC0' + str(index)
            else:
                code = 'AC' + str(index)
            yield self.getPageIndex(code, 1)

    def getPageIndex(self, code, page):
        self.logger.info('|getPageIndex| code %s page %s' % (code, page))
        return scrapy.FormRequest(
            self.getBookCategoryInfo,
            callback=self.parse,
            method='POST',
            formdata={
                'code': code,
                'page': str(page),
                'px': 'desc',
                'limit': '9'
            },
            meta={
                'page': page,
                'code': code
            }
        )

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        is_success = body['success']
        page = response.meta['page']
        code = response.meta['code']
        if is_success:
            for detail in body['module']:
                id = detail['id']
                yield scrapy.Request(url=self.bookDetailPrefix + str(id), callback=self.parseDetail, meta={'detail': detail})

            yield self.getPageIndex(code, page + 1)

    def parseDetail(self, response):
        for href in response.css('.read.readactive a::attr(href)').extract():
            yield response.follow(href, callback=self.parseBook, meta=response.meta)

    def parseBook(self, response):
        detail = response.meta['detail']
        detail['bookUrl'] = response.url

        yield detail
