# !/usr/bin/env python
# -*- coding: UTF-8 -*

#TODO:
#  cache image
#  get update info
#  get current price
#  get minifig info
#  get piece info

import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import parse_brickset
from database import LegoDb

DATABASE = '/home/dormouse/project/legohole/testdata/test.db'
TABLE = 'brickset'

app = Flask(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_sets_table(sql):
    rows = query_db(sql)
    objs = {}

    objs['table_head'] = [ u'编号', u'名称', u'系列', u'子系列', u'价格', 
                u'年份', u'人仔']

    objs['table_body'] = []
    for row in rows:
        row['price'] = '|'.join([item for item in [
            u'$'+row['usprice'] if row['usprice'] else '',
            u'£'+row['ukprice'] if row['ukprice'] else '',
            u'€'+row['euprice'] if row['euprice'] else '',
            ] if item])
        row['price'] = row['price'] if row['price'] else u'无'
        row['subtheme'] = row['subtheme'] if row['subtheme'] else u'无'
        row['minifigs'] = row['minifigs'] if row['minifigs'] else u'无'
        show_items = [ row['id'], row['number']+'-'+row['variant'],
                row['name'], row['theme'], row['subtheme'],
                row['price'], row['year'], row['minifigs']]
        objs['table_body'].append(show_items)
    return objs
    

@app.route('/')
def index():
    sql = 'select * from brickset order by add_time desc limit 10'
    objs = get_sets_table(sql)
    return render_template('index.html', objs=objs)

@app.route('/buy_uk')
def buy_uk():
    objs = {}

    objs['table_head'] = [
            'pic', 'set_number', 'name', 'theme', 'year',
            'price', 'price_rmb', 'discount', 'vendor'
            ]
    #get last update time
    sql = "select * from update_log where content = 'buy_uk' order by end desc"
    row = query_db(sql, args=(), one=True)
    if row:
        sql = "select * from price where datetime >= ? and datetime <= ?"
        args = (row['start'], row['end'])
        prices = query_db(sql, args)
        objs['table_body'] = []
        for p in prices:
            objs['table_body'].append(uk_disc(p))

    return render_template('set_buy_uk.html', objs=objs)

def uk_disc(price):
    """ caculate uk price discount"""
    fields = [
            'thumb_url', 'set_number', 'name', 'theme', 'year',
            'price', 'price_rmb', 'disc', 'vendor'
            ]

    objs = {}
    objs['set_number'] = price['set_number']
    objs['vendor'] = price['vendor']

    #small_pic_url,name,number,theme,year,
    #price_uk,price_uk_rmb,discount
    objs['thumb_url'] = ''.join(
        ("http://images.brickset.com/sets",
         "/thumbs/tn_%s_jpg.jpg"%objs['set_number']))
    db = LegoDb(g.db)
    row = db.query_brickset_by_set_number(objs['set_number'])
    if row:
        objs['name'] = row.get('name')
        objs['theme'] = row.get('theme')
        objs['year'] = row.get('year')
        us_rp = row.get('usprice')

    #得到汇率
    huilv = db.query_huilv()
    gbp_rate = float(huilv['gbp'])/100
    usd_rate = float(huilv['usd'])/100

    #计算折扣
    uk_cp = float(price['price'])
    us_rp_rmb = float(us_rp) * usd_rate 
    #英镑退税后人民币当前价格
    uk_cp_rmb = uk_cp * gbp_rate / 1.2
    #英镑退税后人民币当前价格折扣
    uk_disc = uk_cp_rmb/us_rp_rmb * 100

    objs['price'] = u'£%s'%uk_cp
    objs['price_rmb'] = u'￥%.2f'%uk_cp_rmb
    objs['disc'] = u'%.2f%%'%uk_disc

    data = [objs.get(field) for field in fields]
    print data
    return data


@app.route('/set/number/<set_number>')
def sets_by_number(set_number):
    number, variant = set_number.split('-')
    sql = ' '.join([
            "select * from",
            TABLE,
            "where number=? and variant=?"
            ])
    args = (number, variant)
    row = query_db(sql, args, one=True)
    print 'us$$$', row['usprice']
    show_items = [{'name':u'名称', 'value':row['name']},
            {'name':u'编号', 'value':row['number']+'-'+row['variant']},
            {'name':u'系列', 'value':row['theme']+'-'+row['subtheme']},
            {'name':u'价格', 'value':row['usprice']},
            {'name':u'年份', 'value':row['year']},
            {'name':u'人仔', 'value':row['minifigs']},
            ]
    """
            id integer primary key,
            setid text,
            number text,
            variant text,
            theme text,
            subtheme text,
            year text,
            name text,
            minifigs text,
            pieces text,
            ukprice text,
            usprice text,
            caprice text,
            euprice text,
            imageurl text,
            owned text,
            wanted text,
            qtyowned text,
            add_time text,
            modi_time text,
            data_source text)
            """
    objs = {}
    objs['show_items'] = show_items
    objs['img_url'] = row['imageurl']
    return render_template('set_detail.html', objs=objs)
    
@app.route('/set/id/<set_id>')
def sets_by_id(set_id):
    sql = ' '.join([ "select * from", TABLE, "where id=?"])
    args = (set_id,)
    row = query_db(sql, args, one=True)

    row['price'] = '|'.join([item for item in [
        u'$'+row['usprice'] if row['usprice'] else '',
        u'£'+row['ukprice'] if row['ukprice'] else '',
        u'€'+row['euprice'] if row['euprice'] else '',
        ] if item])

    row['price'] = row['price'] if row['price'] else u'无'
    row['subtheme'] = row['subtheme'] if row['subtheme'] else u'无'
    row['minifigs'] = row['minifigs'] if row['minifigs'] else u'无'

    show_items = [
            {'name':u'编号', 'value':row['number']+'-'+row['variant']},
            {'name':u'名称', 'value':row['name']},
            {'name':u'系列', 'value':row['theme']},
            {'name':u'子系列', 'value':row['subtheme']},
            {'name':u'价格', 'value':row['price']},
            {'name':u'年份', 'value':row['year']},
            {'name':u'人仔', 'value':row['minifigs']},
            ]
    objs = {}
    objs['show_items'] = show_items
    objs['img_url'] = row['imageurl']
    return render_template('set_detail.html', objs=objs)

@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        if request.form['setnumber']:
            sql = ' '.join([
                    "select * from",
                    TABLE,
                    "where number like",
                    "'%"+request.form['setnumber']+"%'",
                    'order by number',
                    ])
            objs = get_sets_table(sql)
            return render_template('set_list.html', objs=objs)

if __name__ == '__main__':
    app.run(debug=True)
