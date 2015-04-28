# !/usr/bin/env python
# -*- coding: UTF-8 -*

import json
import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3 as sqlite

from database import LegoDb

DATABASE = 'test.db'

def write_db(huilv):
    cx = sqlite.connect(DATABASE)
    fields = ('usd', 'gbp', 'eur', 'cad', 'datetime')
    data = ([huilv[field] for field in fields])
    sql = u"insert into huilv (id,usd,gbp,eur,cad,datetime) \
        values (null,?,?,?,?,?)"
    cx.execute(sql, data)
    cx.commit()
    cx.close()

def get_huilv_from_cmb():
    cmb_url = 'http://fx.cmbchina.com/Hq/'
    html_waihui = urllib.urlopen(cmb_url).read()
    huilv = parse_html(html_waihui)
    return huilv

def get_huilv_from_cmb_test():
    with open('test_waihui.html') as f:
        huilv = parse_html(f.read())
    return huilv

def parse_html(html):
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

def debug_print(huilv):
    for i in huilv:
        print i, huilv[i]

def get_huilv_from_db():
    db = LegoDb()
    db.connect_db()
    huilv = db.query_huilv()
    db.disconnect_db()
    return huilv

def get_huilv():
    huilv = get_huilv_from_db()
    if not huilv:
        huilv = get_huilv_from_cmb()
    return huilv

if __name__ == '__main__':
    #init_db()
    #huilv = get_huilv_from_cmb_test()
    huilv = get_huilv_from_cmb()
    debug_print(huilv)
    write_db(huilv)
    





