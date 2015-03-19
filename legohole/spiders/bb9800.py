# -*- coding: utf-8 -*-
import scrapy
from legohole.items import LegoholeItem


class Bb9800Spider(scrapy.Spider):
    name = "bb9800"
    allowed_domains = ["bb9800.diandian.com"]
    start_urls = (
            'http://127.0.0.1:9090/bb9800.html',
    )
    #    'http://bb9800.diandian.com/',
    def _get_text(self, res, path):
        strings = res.xpath(path).extract()
        return ''.join(strings).strip()

    def _get_list(self, res, path):
        strings = res.xpath(path).extract()
        return strings

    def parse(self, response):
        #get all post links
        post_links = response.xpath(
                '//div[@class="list clearfix"]//p[@id="time"]/a/@href').extract()
        for link in post_links[:3]:
            print link
            yield scrapy.Request(link, callback=self.parse_post)

        #get next page
        next_pages = response.xpath('//a[@class="page_next"]/@href').extract()
        if len(next_pages) == 1:
            print next_pages[0]
            #yield scrapy.Request(next_page[0])

    def parse_post(self, response):
        item = LegoholeItem()
        item['tags'] = self._get_list(response,
                '//div[@class="list clearfix"]//li/a/text()')
        item['time'] = self._get_text(response,
                '//div[@class="list clearfix"]//p[@id="time"]/a/text()')
        yield item
        """
        title = response.xpath('//h1/text()').extract()
        texts = response.xpath('//div[@id="byline"]/text()')
        publish_time = (texts.extract()[0].split("\r\n")[1]).strip()
        contents = response.xpath('//div[@class="content"]/p')

        print title
        print publish_time
        """

