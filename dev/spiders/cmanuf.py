import scrapy

class Cmanuf(scrapy.Spider):
    name = 'cmanuf'
    start_urls = ['http://ebooks.cmanuf.com/all?id=1&type=2&code=AC01']

    def parse(self, response):
        filename = 'xxx.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
