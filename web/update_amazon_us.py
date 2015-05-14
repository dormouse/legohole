# !/usr/bin/env python
# -*- coding: UTF-8 -*

import re
import random
import sys
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from urllib import urlopen

from database import LegoDb

#获得美国亚马逊直邮中国LEGO的价格

import logging

class AmazonUS():
    """查询 amazon us 网站"""

    def __init__(self):
        #setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('update_amazon_us.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        self.start_url = """
        http://www.amazon.com/s/ref=sr_nr_p_89_6?rh=n%3A165793011%2Ck%3Alego%2Cp_n_shipping_option-bin%3A3242350011%2Cp_6%3AATVPDKIKX0DER%2Cp_89%3ALEGO|LEGO+Movie|LEGO+Education|LEGO+Creator+Expert|Duplo&sort=price-desc-rank&keywords=lego&ie=UTF8
        """

    def test(self):
        f = webdriver.Firefox()
        f.get(self.start_url)
        print self.parse_html(f)

    def parse_html(self, f):
        """
        function:
            分析 amazon us 搜索页面
        return:
            item:title, asin, price
            next_page
        """

        ul = f.find_element_by_id('s-results-list-atf')
        lis = ul.find_elements_by_tag_name('li')

        #No item?
        if len(lis) == 0:
            self.logger.error("no item in page.page save as error_z_us.html")
            with open('error_z_us.html', 'w') as f:
                f.write(html.eocode('utf-8'))
            return None

        #get items
        items = filter(None, [self.parse_li(li) for li in lis])

        #next page
        try:
            tag_a = f.find_element_by_id('pagnNextLink')
        except:
            tag_a = None

        obj={"items": items, "next_page": tag_a}
        return obj

    def parse_li(self, li):
        """
        function:
            parse single div of item
        return:
            dict like {
                'datetime': '20150514121346',
                'price': u'60.81',
                'item_url': u'http://www.amazon.com/
                    LEGO-Education-Community-Vehicles-4562972/dp/B0085Y3T06/
                    ref=sr_1_24/177-6770848-2084811......
               'vendor': u'amazon_us',
               'title': u'LEGO Education DUPLO Community Vehicles Set 4562972
                (56 Pieces)'
            }
        """

        asin = li.get_attribute('data-asin')
        if not asin:
            return None
        tag_a = li.find_elements_by_tag_name('a')[0]
        item_url = tag_a.get_attribute('href')
        title = li.find_element_by_tag_name('h2').text
        tag_span = li.find_element_by_xpath(
            ".//span[@class='a-size-base a-color-price s-price a-text-bold']")
        price = tag_span.text[1:]

        # init return obj 
        obj = {
            'asin':asin,
            'vendor':u'amazon_us',
            'price': price,
            'title': title,
            'item_url': item_url,
            'datetime': datetime.now().strftime("%Y%m%d%H%M%S"),
        }

        return obj

    def write_db(self):
        """把价格写入数据库"""
        obj = {}
        db = LegoDb()
        db.connect_db()
        obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
        f = webdriver.Firefox()
        f.get(self.start_url)
        result = self.parse_html(f)
        if result:
            tag_a = result['next_page']
            items = result['items']
            db.append_prices(items)
            while tag_a:
                tag_a.click()
                result = self.parse_html(f)
                if result:
                    tag_a = result['next_page']
                    items = result['items']
                    db.append_prices(items)
                else:
                    tag_a = None

        obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
        obj['content'] = 'amazon_us'
        db.append_update_log(obj)
        db.disconnect_db()

    def guess(self):
        """
        function:
            according title guess lego number
        """
        #for test
        db = LegoDb()
        db.connect_db()
        row = db.query_update_log('amazon_us')
        if row:
            sql = """
                select * from price
                where datetime >= ? and datetime <= ? and
                instr(vendor, ?)
                """
            args = (row['start'], row['end'], 'amazon_us')
            rows = db.query_db(sql, args)
        have_name = 0

        for row in rows:
            name = row['title'].strip()
            print name
            if name[:4] == u"LEGO":
                sql = """
                    select number, 'LEGO'||' '||theme||' '||name as fullname
                    from brickset where fullname = ?
                    """
                args = (name,)
                num_rows = db.query_db(sql, args)
                if len(num_rows) == 1:
                    print num_rows[0]['number']
                    have_name += 1
                else:
                    sql = """
                        select number 
                        from brickset where name = ?
                        """
                    realname = ' '.join(name.split()[2:])
                    args = (realname,)
                    num_rows = db.query_db(sql, args)
                    if len(num_rows) == 1:
                        print num_rows[0]['number']
                        have_name += 1

        print have_name, len(rows)



        db.disconnect_db()


if __name__ == "__main__":
    AmazonUS().guess()
