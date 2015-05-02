# !/usr/bin/env python
# -*- coding: UTF-8 -*

import os
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
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-'
    prices = []
    for i in range(1,4):
        html = urllib.urlopen(base_url + buy_uk_url + '%s'%i).read()
        prices += parse_buy_uk(html)

        print base_url + buy_uk_url + '%s'%i
    print len(prices)
    return prices

def parse_buy_uk(html):
    """分析英国折扣页面"""

    soup = BeautifulSoup(html)
    table = soup.find_all('table', class_='neattable')[0]
    trs = table.tbody.find_all('tr')
    prices = filter(None, [parse_buy_uk_tr(tr) for tr in trs])
    for p in prices:
        p['discount'] = calc_disc(p)
    return prices

def parse_buy_uk_tr(tr):
    """分析英国折扣页面每一行的数据"""

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
    obj['local'] = 'uk'

    return obj

def get_huilv_from_db(local):
    db = LegoDb()
    db.connect_db()
    row = db.query_huilv()
    db.disconnect_db()
    try:
        rate = float(row[local])/100
    except:
        print "can not get %s exchange rate"%local
        rate = None
    return rate

def calc_disc(price):
    """ calc discount"""

    #check number and price
    try:
        number = price['set_number']
        cp = float(price['price'])
    except:
        print 'can not get set_number and price'
        return None

    db = LegoDb()

    #得到美元零售人民币价格
    usd_rate = get_huilv_from_db('usd')
    if not usd_rate:
        return None
    db.connect_db()
    row = db.query_brickset(True, 'usprice', number=number)
    db.disconnect_db()
    if row and row['usprice']:
        us_rp_rmb = float(row['usprice'])*usd_rate
    else:
        return None

    cp_rmb = None
    if price['local'] == 'uk':
        #得到英镑汇率
        gbp_rate = get_huilv_from_db('gbp')
        if not gbp_rate:
            return None
        #英镑退税后人民币当前价格
        cp_rmb = cp*gbp_rate/1.2

    if price['local'] == 'cn':
        cp_rmb = cp

    if cp_rmb:
        disc = round(cp_rmb/us_rp_rmb*100, 2) 
    else:
        disc = None
    return disc 

def update_buy_uk():
    """把价格写入数据库"""
    obj = {}
    db = LegoDb()
    db.connect_db()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    prices = get_buy_uk()
    db.append_prices(prices)
    down_thumbs(prices)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'buy_uk'
    db.append_update_log(obj)
    db.disconnect_db()

def update_huilv():
    """ update huilv """

    obj = {}
    db = LegoDb()
    db.connect_db()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    huilv = get_huilv_from_cmb()
    db.append_huilv(huilv)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'huilv'
    db.append_update_log(obj)
    db.disconnect_db()

def update_db():
    update_huilv()
    update_buy_uk()

def down_thumbs(prices):
    urls = [make_thumb_url(price['set_number']) for price in prices]
    target_path = "/home/dormouse/project/legohole/web/static/pic/thumb"
    for url in urls:
        download(url, target_path)
    #http://images.brickset.com/sets/images/70706-1.jpg
    #http://images.brickset.com/sets/large/70706-1.jpg
def make_thumb_url(set_number):
    imgurl = ''.join(
        ('http://images.brickset.com/sets',
         '/thumbs/tn_%s_jpg.jpg'%set_number))
    return imgurl

def download(url, target_path):
    fname = os.path.join(target_path, url.split('/')[-1])
    if not os.path.exists(fname):
        os.system("wget -nv -P %s %s"%(target_path, url))

def test():
    base_url = 'http://brickset.com'
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
    html = urllib.urlopen(base_url + buy_uk_url).read()
    prices = parse_buy_uk(html)
    db = LegoDb()
    db.connect_db()
    db.append_prices(prices[:3])
    db.disconnect_db()
    print len(prices)
    print prices[:3]

if __name__ == '__main__':
    update_db()
    #test()

