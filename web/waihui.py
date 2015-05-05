# !/usr/bin/env python
# -*- coding: UTF-8 -*

import json
import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3 as sqlite

from database import LegoDb

DATABASE = 'test.db'

def write_db(exrate):
    cx = sqlite.connect(DATABASE)
    fields = ('usd', 'gbp', 'eur', 'cad', 'datetime')
    data = ([exrate[field] for field in fields])
    sql = u"insert into exrate (id,usd,gbp,eur,cad,datetime) \
        values (null,?,?,?,?,?)"
    cx.execute(sql, data)
    cx.commit()
    cx.close()

def get_exrate_from_cmb():
    cmb_url = 'http://fx.cmbchina.com/Hq/'
    html_waihui = urllib.urlopen(cmb_url).read()
    exrate = parse_html(html_waihui)
    return exrate

def get_exrate_from_cmb_test():
    with open('test_waihui.html') as f:
        exrate = parse_html(f.read())
    return exrate

def parse_html(html):
    bs = BeautifulSoup(html)
    exrate  = {}
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
                exrate[name['name_en']] = tds[5]
        #获得时间
        time = ''.join(tds[8].split(':'))
    #获得时间
    #当前日期：2015年04月21日
    td_texts = [td.text.strip() for td in bs.find_all("td")]
    for text in td_texts:
        if text.startswith(u"当前日期："):
            date = ''.join((text[5:9], text[10:12], text[13:15]))
    exrate['datetime'] = ''.join((date, time))

    #TODO:验证数据
    return exrate

def debug_print(exrate):
    for i in exrate:
        print i, exrate[i]

def get_exrate_from_db():
    db = LegoDb()
    db.connect_db()
    exrate = db.query_exrate()
    db.disconnect_db()
    return exrate

def get_exrate():
    exrate = get_exrate_from_db()
    if not exrate:
        exrate = get_exrate_from_cmb()
    return exrate

if __name__ == '__main__':
    #init_db()
    #exrate = get_exrate_from_cmb_test()
    exrate = get_exrate_from_cmb()
    debug_print(exrate)
    write_db(exrate)
    





