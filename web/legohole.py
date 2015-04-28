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
import json

import parse_brickset
from database import LegoDb
from cn_amazon_price import Amazon

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
        show_items = [ row['id'], row['number'],
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
    table_head_field = ['pic', 'detail', 'price', 'price_rmb',
                        'discount', 'vendor']

    table_head_zh = [u'图片', u'说明', u'英镑', u'人民币',
                     u'折扣', u'供货商']

    objs['table_head'] = zip(table_head_field, table_head_zh)

    return render_template('set_buy_uk.html', objs=objs)

@app.route('/ajax/buy_uk')
def ajax_buy_uk():
    #get last update time
    db = LegoDb(g.db)
    row = db.query_update_log('buy_uk')
    if row:
        prices = db.query_price(row['start'], row['end'], 'amazon_uk')
        uk_buy_table_body = [uk_disc(p) for p in prices]
        return json.dumps(uk_buy_table_body)
    else:
        return None


def uk_disc(price):
    """ caculate uk price discount"""
    fields = ['thumb_url', 'set_number', 'name', 'theme', 'year',
              'price', 'price_rmb', 'disc', 'vendor']

    obj = {}
    set_number = price['set_number']

    html = '<a href="%s"><span class="label label-info">%s</span></a>'
    set_number_html = html%(
            url_for('sets_by_number',set_number=set_number),
            set_number)

    obj['vendor'] = price['vendor']

    #small_pic_url,name,number,theme,year,
    #price_uk,price_uk_rmb,discount
    thumb_url = "/static/pic/thumb"
    obj['pic'] = '<img src ="%s/tn_%s_jpg.jpg">'%(thumb_url, set_number)

    db = LegoDb(g.db)
    row = db.query_brickset(True, number=set_number)
    if row:
        name = row.get('name')
        theme = row.get('theme')
        subtheme = row.get('subtheme')
        year = row.get('year')
        us_rp = row.get('usprice')

    html = '<span class="label label-info">%s</span>'
    theme_html = html%(theme,)
    subtheme_html = html%(subtheme,)
    year_html = html%(year,)
    obj['detail'] = '<h4>%s<h4>%s %s %s %s'%(name, set_number_html,
            theme_html, subtheme_html, year_html)

    #得到汇率
    huilv = db.query_huilv()
    gbp_rate = float(huilv['gbp'])/100
    usd_rate = float(huilv['usd'])/100

    #计算折扣
    uk_cp = float(price['price'])
    obj['price'] = uk_cp
    #英镑退税后人民币当前价格
    uk_cp_rmb = uk_cp * gbp_rate / 1.2
    obj['price_rmb'] = round(uk_cp_rmb, 2)
    try:
        us_rp_rmb = float(us_rp) * usd_rate 
        us_rp_rmb = float(us_rp) * usd_rate 
        #英镑退税后人民币当前价格折扣
        uk_disc = round(uk_cp_rmb/us_rp_rmb*100, 2) 
        obj['discount'] = uk_disc
    except:
        pass

    return obj

@app.route('/ajax/get_amazon_cn/number/<set_number>')
def get_amazon_cn(set_number):
    number = set_number.split('-')[0]
    price = Amazon().get_lego_price(number)
    return price

@app.route('/set/number/<set_number>')
def sets_by_number(set_number):
    sql = ' '.join([ "select * from", TABLE, "where number=?" ])
    args = (set_number, )
    row = query_db(sql, args, one=True)
    objs = show_set(row)
    return render_template('set_detail.html', objs=objs)

    
@app.route('/set/id/<set_id>')
def sets_by_id(set_id):
    sql = ' '.join([ "select * from", TABLE, "where id=?"])
    args = (set_id,)
    row = query_db(sql, args, one=True)
    objs = show_set(row)
    return render_template('set_detail.html', objs=objs)

def show_set(row):
    row['price'] = '|'.join([item for item in [
        u'$'+row['usprice'] if row['usprice'] else '',
        u'£'+row['ukprice'] if row['ukprice'] else '',
        u'€'+row['euprice'] if row['euprice'] else '',
        ] if item])

    row['price'] = row['price'] if row['price'] else u'无'
    row['subtheme'] = row['subtheme'] if row['subtheme'] else u'无'
    row['minifigs'] = row['minifigs'] if row['minifigs'] else u'无'

    show_items = [
            {'name':u'编号', 'value':row['number']},
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
    return objs

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
