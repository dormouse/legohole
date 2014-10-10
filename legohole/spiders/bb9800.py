# -*- coding: utf-8 -*-
import scrapy


class Bb9800Spider(scrapy.Spider):
    name = "bb9800"
    allowed_domains = ["bb9800.diandian.com"]
    start_urls = (
        'http://www.bb9800.diandian.com/',
    )

    def parse(self, response):
        pass
