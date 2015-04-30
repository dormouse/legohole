# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import datetime

import parse_brickset
from waihui import get_huilv

from database import LegoDb

"""
base_url = 'http://brickset.com'
buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
text = urlopen(base_url + buy_uk_url).read()
soup = BeautifulSoup(text)
divs = soup.find_all('div', class_='tags hideonmediumscreen')
for div in divs:
    set_url = base_url + div.a['href']
"""
def test_url():
    url = 'http://cn.ipricetracker.com/search?type=amazon&q=lego+60044'
    html = urlopen(url).read()
    with open('aa.html','w') as f:
        f.write(html)
    #print parse_html(html)

def test_uk_text():
    """测试本地文档"""
    with open('buy_uk.html') as f:
        parse_buy_UK(f.read())

def parse_html(html):

    soup = BeautifulSoup(html)
    tr = soup.find_all('tr', class_='search_tr')[0]
    div = tr.find_all('div', class_='price')[0]
    print div.text


def parse_buy_uk_tr(tr):

    obj = {}
    tds = tr.find_all('td')
    obj['set_number'] = tds[1].div.a.text

    if tds[2].text == u'(Marketplace)':
        obj['vendor'] = u'amazon_uk_MP'
    else:
        obj['vendor'] = u'amazon_uk'

    price_span = tr.find_all('span', class_='price')[0]
    price = price_span.text
    obj['price'] = price[1:] 

    obj['datetime'] = datetime.now().strftime("%Y%m%d%H%M%S")

    return obj

def write_db(prices):
    """把价格写入数据库"""
    obj = {}
    db = LegoDb()
    db.connect_db()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    db.append_prices(prices)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'buy_uk'
    db.append_update_log(obj)
    db.disconnect_db()


    
if __name__ == "__main__":
    test_url()
