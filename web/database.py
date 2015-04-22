# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
from datetime import datetime

DATABASE = 'test.db'

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
        
    def create_view(self, name):
        self.connect_db()
        if name == 'brickset_number_view':
            self.cx.execute("drop view if exists brickset_number_view")
            sql = """
                CREATE VIEW brickset_number_view AS 
                SELECT id, number||'-'||variant as set_number FROM brickset
            """
            self.cx.execute(sql)
        self.disconnect_db()

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

    def query_brickset_by_setid(self, setid):
        """查询 brickset 表中 setid 是否存在"""

        sql = 'select * from brickset where setid = ?'
        args = (setid,)
        rvs = self.query_db(sql, args)
        found_rows = len(rvs)
        if found_rows == 1:
            return True
        if found_rows == 0:
            return False
        if found_rows > 1:
            print 'error:mulity setid:%s'%(args[0])
            return False

    def get_id_by_set_number(self, set_number):
        """根据 set_number 查询 id """

        sql = """
            select id from brickset_number_view
            where set_number = ?
        """
        args = (set_number,)
        row = self.query_db(sql, args, True)
        return row['id'] if row else None

    def query_brickset_by_id(self, set_id):
        """根据 id 查询 brickset 表 """

        sql = 'select * from brickset where id = ?'
        args = (set_id,)
        row = self.query_db(sql, args, True)
        return row

    def query_brickset_by_set_number(self, set_number):
        """根据 set_number 查询 brickset 表 """
        set_id = self.get_id_by_set_number(set_number)
        if set_id:
            row = self.query_brickset_by_id(set_id)
        return row

    def query_huilv(self):
        now = datetime.now()
        cur_date = now.strftime("%Y%m%d")
        sql = 'select * from huilv where datetime > ?'
        args = (cur_date,)
        row = self.query_db(sql, args, True)
        return row

    def append_prices(self,prices):
        """write price to db"""
        fields = ('set_number', 'price', 'vendor', 'datetime')
        for price in prices:
            data = ([price[field] for field in fields])
            sql = u"insert into price (id,set_number,price,vendor,datetime) \
                values (null,?,?,?,?)"
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
    db.disconnect_db()

