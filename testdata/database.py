# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
from datetime import datetime

DATABASE = '/home/dormouse/project/legohole/testdata/test.db'

class LegoDb():
    """LEGO 数据库"""

    def __init__(self,cx=None):
        if cx:
            self.cx = cx
        else:
            self.db_name = 'test.db'

    def connect_db(self):
        self.cx = sqlite.connect(DATABASE)

    def disconnect_db(self):
        self.cx.close()
        
    def create_table(self, name):
        self.connect_db()
        if name == 'brickset':
            self.cx.execute("drop table if exists brickset")
            init_sql = """create table brickset (
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
                    data_source text)"""
            self.cx.execute(init_sql)

        if name == 'huilv':
            self.cx.execute("drop table if exists huilv")
            init_sql = """create table huilv (
                    id integer primary key,
                    usd text,
                    gbp text,
                    eur text,
                    cad text,
                    datetime text
                    )"""
            self.cx.execute(init_sql)

        if name == 'price':
            self.cx.execute("drop table if exists price")
            init_sql = """create table price (
                    id integer primary key,
                    set_number text,
                    price text,
                    discount text,
                    vendor text,
                    datetime text
                    )"""
            self.cx.execute(init_sql)

        if name == 'update_log':
            self.cx.execute("drop table if exists update_log")
            init_sql = """create table update_log(
                    id integer primary key,
                    start text,
                    end text,
                    content text
                    )"""
            self.cx.execute(init_sql)

        self.disconnect_db()

    def query_db(self, sql, args=(), one=False):
        cur = self.cx.execute(sql, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def query_brickset_by_brickset_id(self, brickset_id):
        """查询 brickset 表中 setid 是否存在"""

        sql = 'select * from brickset where brickset_id = ?'
        args = (brickset_id,)
        rvs = self.query_db(sql, args)
        found_rows = len(rvs)
        if found_rows == 1:
            return True
        if found_rows == 0:
            return False
        if found_rows > 1:
            print 'error:mulity setid:%s'%(args[0])
            return False

    def query_brickset(self, one=False, *fields, **filters):
        """
        功能：
            查询 brickset 表
        参数：
            one    ：是否只返回一条记录
            fields ：返回的字段名称
            filters：查询条件
        """
        fieldstr = ','.join(fields) if fields else '*'
        if filters:
            flist = [(k,v) for k,v in filters.items()]
            wlist = ["%s = ?"%k for k,v in flist]
            wherestr = 'where ' + ' and '.join(wlist)
            args = [v for k,v in flist]
        else:
            wherestr = ''
            args = ()

        sql = ' '.join(['select', fieldstr, 'from brickset', wherestr])

        #print sql
        #print args
        return self.query_db(sql, args, one)

    def query_huilv(self):
        sql = 'select * from huilv order by datetime desc'
        row = self.query_db(sql, one = True)
        return row

    def query_price(self, start, end, vendor):
        sql = """
            select * from price
            where datetime >= ?
                and datetime <= ?
                and instr(vendor, ?)
        """
        args = (start, end, vendor)
        rows = self.query_db(sql, args)
        return rows

    def query_update_log(self,content):
        sql = "select * from update_log where content = ? order by end desc"
        args = (content,)
        row = self.query_db(sql, args, one=True)
        return row

    def append_db(self, table, fields, datas):
        sql = '' .join([
            "insert into %s"%table,
            "(id,%s)"%','.join(fields),
            "values (null,%s)"%','.join('?'*len(fields))
        ])
        for data in datas:
            args = ([data[field] for field in fields])
            self.cx.execute(sql, args)
        self.cx.commit()


    def append_prices(self,prices):
        """write price to db"""

        fields = ('set_number', 'price', 'discount', 'vendor', 'datetime')
        self.append_db('price', fields, prices)


    def append_huilv(self, huilv):
        """ append current huilv to db"""

        fields = ('usd', 'gbp', 'eur', 'cad', 'datetime')
        data = ([huilv[field] for field in fields])
        sql = u"insert into huilv (id,usd,gbp,eur,cad,datetime) \
            values (null,?,?,?,?,?)"
        self.cx.execute(sql, data)
        self.cx.commit()

    def append_update_log(self,log):
        """write update_log to db"""
        fields = ('start', 'end', 'content')
        data = ([log[field] for field in fields])
        sql = u"insert into update_log(id,start,end,content)\
                values (null,?,?,?)"
        self.cx.execute(sql, data)
        self.cx.commit()

if __name__ == '__main__':
    db = LegoDb()
    db.connect_db()
    #print LegoDb().query_brickset_setid('8088')
    #LegoDb().create_view('brickset_number_view')
    #print db.query_brickset_by_set_number('60052-1')
    #print db.query_huilv()
    db.create_table('price')
    
    #db.query_brickset(True, 'number', id='333', number=444)
    #db.query_brickset(True, id='333', number=444)
    #db.query_brickset(True)
    db.disconnect_db()

