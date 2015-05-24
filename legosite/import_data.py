# !/usr/bin/env python
# -*- coding: UTF-8 -*
# Import test data for django site develop.


import csv
import sqlite3 as sqlite
import glob
from datetime import datetime

OLD_DB = '/home/dormouse/project/legohole/testdata/test.db'
NEW_DB = '/home/dormouse/project/legohole/legosite/db.sqlite3'

def query_db(cx, sql, args=(), one=False):
    cur = cx.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row))
            for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def append_db(cx, table, fields, datas):
    print datas
    """
    function:
        append datas to db
    Note:
        datas can be list or dict
    """

    sql = '' .join([
        "insert into %s"%table,
        "(id,%s)"%','.join(fields),
        "values (null,%s)"%','.join('?'*len(fields))
    ])

    if isinstance(datas, list):
        args = [([data.get(field) for field in fields]) for data in datas]
        cx.executemany(sql, args)
    else:
        for data in datas:
            args = ([datas.get(field) for field in fields])
        cx.execute(sql, args)
    cx.commit()

def covert_discount(row, cx_new):
    number = row['set_number']
    sql = """
        select id from legosets_legoset where number = ?
    """
    args = (number,)
    legoset_row = query_db(cx_new, sql, args, one=True)
    number_id = legoset_row['id']
    
    vendor_id = 0 #default
    vendor = row['vendor']
    if vendor == 'amazon_uk':
        vendor_id = 1
    if vendor == 'amazon_uk_MP':
        vendor_id = 2

    try:
        discount = int(round(row['discount']))
    except:
        discount = 0

    data = {
        'number_id': number_id,
        'vendor_id': vendor_id,
        'discount': discount,
    }
    return data

def covert_legoset(row):
    datetime = row['add_time']
    dates = datetime.split()
    add_datetime = ' '.join(dates[:-1])+'.'+dates[-1]
    modi_datetime = add_datetime
    data = {
        'number': row['number'],
        'name': row['name'],
        'add_datetime': add_datetime,
        'modi_datetime': modi_datetime,
        }
    return data

def import_data():
    cx_new = sqlite.connect(NEW_DB)
    cx_old = sqlite.connect(OLD_DB)
    
    #clean table
    tables = ('legosets_legoset', 'legosets_vendor', 'legosets_discount')
    for table in tables:
        sql = 'delete from %s'%table
        cx_new.execute(sql)
        sql = 'delete from sqlite_sequence where name=?'
        args = (table,)
        cx_new.execute(sql, args)

    #import legoset
    sql = "select number,name,add_time from brickset"
    rows = query_db(cx_old, sql)
    datas = [covert_legoset(row) for row in rows]
    table = 'legosets_legoset'
    fields = ('number', 'name', 'add_datetime', 'modi_datetime')
    sql = '' .join([
        "insert into %s"%table,
        "(id,%s)"%','.join(fields),
        "values (null,?,?,datetime(?),datetime(?))"
    ])
    args = [([data.get(field) for field in fields]) for data in datas]
    cx_new.executemany(sql, args)

    
    #import vendor
    table = 'legosets_vendor'
    fields = ('name',)
    datas = [{'name':'amazon_uk'}, {'name':'amazon_uk_MP'}]
    append_db(cx_new, table, fields, datas)
    
    #import discount
    sql = """
        select set_number,vendor,discount from price
        where datetime >= ? and datetime <= ?
    """
    args = ('20150509205342', '20150509205354')
    rows = query_db(cx_old, sql, args)
    datas = [covert_discount(row, cx_new) for row in rows]
    table = 'legosets_discount'
    fields = ('discount', 'number_id', 'vendor_id')
    append_db(cx_new, table, fields, datas)

    cx_new.close()
    cx_old.close()

if __name__ == '__main__':
    import_data()
