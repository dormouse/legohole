# !/usr/bin/env python
# -*- coding: UTF-8 -*

import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

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

@app.route('/')
def index():
    sql = 'select * from brickset order by add_time desc limit 10'
    sets = query_db(sql)
    return render_template('index.html', sets=sets)

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
            sets = query_db(sql)
            return render_template('set_list.html', sets=sets)

if __name__ == '__main__':
    app.run(debug=True)
