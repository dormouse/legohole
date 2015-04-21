# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from urllib import urlopen

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
def test_uk_text():
    """测试本地文档"""
    with open('buy_uk.html') as f:
        parse_buy_UK(f.read())

def parse_buy_UK(html):
    """分析英国折扣页面"""

    soup = BeautifulSoup(html)
    divs = soup.find_all('div', class_='tags hideonmediumscreen')
    set_numbers = [div.a.string for div in divs]
    for number in set_numbers[:4]:
        output(number)

def output(set_number):
    """输出结果"""
    obj = {}

    db = LegoDb()
    db.connect_db()

    #small_pic_url,name,number,theme,year,
    #price_uk,price_uk_rmb,discount
    obj['thumb_url'] = ''.join(("http://images.brickset.com",
                               "/sets/thumbs/tn_%s_jpg.jpg"%set_number))
    row = db.query_brickset_by_set_number(set_number)
    if row:
        obj['name'] = row.get('name')
        obj['theme'] = row.get('theme')
        obj['year'] = row.get('year')

    #得到汇率
    huilv = get_huilv()
    gbp_rate = float(huilv['gbp'])
    usd_rate = float(huilv['usd'])

    #计算折扣
    prices = parse_brickset.get_brickset_price_by_set_number(set_number)
    #英镑退税后人民币当前价格
    uk_cp_rmb = prices['UK']['cp'] * gbp_rate / 1.2

    if prices.has_key('US'):
        #美元人民币当前价格
        us_cp_rmb = prices['US']['cp'] * usd_rate
        #美元人民币零售价格
        us_rp_rmb = prices['US']['rp'] * usd_rate
        #美元人民币当前价格折扣
        us_disc = us_cp_rmb/us_rp_rmb * 100
        obj['price_us'] = u'£%s'%prices['US']['cp']
        obj['price_us_rmb'] = u'￥%.2f'%us_cp_rmb
        obj['disc_us'] = u'%.2f%%'%us_disc
    else:
        us_rp_rmb = float(row['usprice']) * usd_rate 

    #英镑退税后人民币当前价格折扣
    uk_disc = uk_cp_rmb/us_rp_rmb * 100

    obj['price_uk'] = u'£%s'%prices['UK']['cp']
    obj['price_uk_rmb'] = u'￥%.2f'%uk_cp_rmb
    obj['disc_uk'] = u'%.2f%%'%uk_disc


    print obj

    """
    prices = get_brickset_price_by_setid(set_id)
    print set_id
    if prices.has_key('UK') and prices.has_key('US'):
        #format output
        print u'£%s'%prices['UK']['cp'],'\t',
        print u'￥%.2f'%prices['UK']['cp_rmb'],'\t',
        print u'%.2f%%'%(prices['UK']['cp_disc']*100),'\t',

        print u'$%s'%prices['US']['cp'],'\t',
        print u'￥%.2f'%prices['US']['cp_rmb'],'\t',
        print u'%.2f%%'%(prices['US']['cp_disc']*100),'\t'
    """

    db.disconnect_db()
    
if __name__ == "__main__":
    test_uk_text()
