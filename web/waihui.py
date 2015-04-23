# !/usr/bin/env python
# -*- coding: UTF-8 -*

import json
import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3 as sqlite
from datetime import datetime

from database import LegoDb

def get_huilv_from_cmb():
    """ get huilv from china merchants bank"""
    cmb_url = 'http://fx.cmbchina.com/Hq/'
    html_waihui = urllib.urlopen(cmb_url).read()
    huilv = parse_huilv_html(html_waihui)
    return huilv

def parse_huilv_html(html):
    bs = BeautifulSoup(html)
    huilv  = {}
    names = (
            (u'美元', u'usd'),
            (u'英镑', u'gbp'),
            (u'欧元', u'eur'),
            (u'加拿大元', u'cad'),
    )
    field_name = ('name_zh', 'name_en')
    waihui_names = [dict(zip(field_name, name)) for name in names]
    #获得汇率
    for tr in bs.select("#realRateInfo")[0].find_all("tr"):
        tds = [td.text.strip() for td in tr.find_all("td")]
        for name in waihui_names: 
            if tds[0] == name['name_zh']:
                huilv[name['name_en']] = tds[5]
        #获得时间
        time = ''.join(tds[8].split(':'))
    #获得时间
    #当前日期：2015年04月21日
    td_texts = [td.text.strip() for td in bs.find_all("td")]
    for text in td_texts:
        if text.startswith(u"当前日期："):
            date = ''.join((text[5:9], text[10:12], text[13:15]))
    huilv['datetime'] = ''.join((date, time))

    #TODO:验证数据
    return huilv

def get_buy_uk():
    """get disc of amazon uk from briceset"""

    base_url = 'http://brickset.com'
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
    html = urllib.urlopen(base_url + buy_uk_url).read()
    return parse_buy_uk(html)

def parse_buy_uk(html):
    """分析英国折扣页面"""

    soup = BeautifulSoup(html)
    table = soup.find_all('table', class_='neattable')[0]
    trs = table.tbody.find_all('tr')
    prices = [parse_buy_uk_tr(tr) for tr in trs]
    return prices

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

def update_buy_uk():
    """把价格写入数据库"""
    obj = {}
    db = LegoDb()
    db.connect_db()
    prices = get_buy_uk()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    db.append_prices(prices)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'buy_uk'
    db.append_update_log(obj)
    db.disconnect_db()

def update_huilv():
    """ update huilv """

    obj = {}
    huilv = get_huilv_from_cmb()
    db = LegoDb()
    db.connect_db()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    db.append_huilv(huilv)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'huilv'
    db.append_update_log(obj)
    db.disconnect_db()

def update_db():
    #update_huilv()
    update_buy_uk()

if __name__ == '__main__':
    update_db()

