# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re

class TvScheduleSpider(scrapy.Spider):
    name = 'tv_schedule'
    allowed_domains = ['www.rrys2019.com']
    start_urls = ['http://www.rrys2019.com/tv/schedule/']
    title_css = 'h2 .corner::text'
    day_css = 'td.ihbg'

    def parse(self, response):
        self.logger.info("URL: %s", response.url)

        title = response.css(self.title_css).extract_first()
        self.logger.info('TITLE: %s', title)

        day_htmls = response.css(self.day_css).extract()   

        item = {
            'title': title,
            'days': self._parse_days(day_htmls)
        }

        yield item
    
    def _parse_days(self, day_htmls):
        dict = {}
        for day_html in day_htmls:
            soup = BeautifulSoup(day_html, 'lxml')
            day_title = soup.find('dt').text
            dict[day_title] = self._parse_day(soup)  
        return dict

    def _parse_day(self, soup):
        resource_links = soup.find_all('a')
        resources = {}
        regex = re.compile(r'\d+', re.IGNORECASE)
        for link in resource_links:
            href = regex.findall(link['href'])[0]
            if href in resources:
                resources[href].append(link.text)
            else:
                resources[href] = [link.text]
        return resources
        

