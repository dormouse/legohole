# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
import datetime

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

        if name == 'exrate':
            self.cx.execute("drop table if exists exrate")
            init_sql = """create table exrate (
                    id integer primary key,
                    usd text,
                    gbp text,
                    eur text,
                    cad text,
                    datetime text
                    )"""
            self.cx.execute(init_sql)

        if name == 'bshtml':
            #raw html of brickset
            self.cx.execute("drop table if exists bshtml")
            init_sql = """create table bshtml (
                    id integer primary key,
                    status_code INTEGER,
                    lego_number text,
                    url text,
                    html text,
                    datetime text,
                    tag text
                    )"""
            self.cx.execute(init_sql)

        if name == 'price':
            self.cx.execute("drop table if exists price")
            init_sql = """CREATE TABLE "price" (
                "id" integer PRIMARY KEY ,
                "set_number" text,
                "price" text,
                "discount" float DEFAULT (null) ,
                "vendor" text,
                "datetime" text
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

    def query_db(self, sql, args=(), one=False):
        cur = self.cx.execute(sql, args)
        rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row))
                for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

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
            wherestr = 'where ' + ' and '.join(
                ["%s=?"%k for k,v in filters.items()]
            )
            args = [v for k,v in filters.items()]
        else:
            wherestr = ''
            args = ()

        sql = ' '.join(['select', fieldstr, 'from brickset', wherestr])

        #print sql
        #print args
        return self.query_db(sql, args, one)

    def query_exrate(self):
        sql = 'select * from exrate order by datetime desc'
        row = self.query_db(sql, one = True)
        return row

    def query_price(self, start, end, vendor, price_filter):
        #check filter
        avaliable_filter = ['theme', 'subtheme', 'year', 'discount']
        for k,v in price_filter:
            if k not in avaliable_filter:
                return None
        wheres = ['where datetime >= ?', 'datetime <= ?', 'instr(vendor, ?)']
        args = [start, end, vendor]
        wheres += ["%s=?"%k for k,v in price_filter if k != 'discount']
        args += [v for k,v in price_filter if k != 'discount']
        wheres += ["%s<=?"%k for k,v in price_filter if k == 'discount']
        args += [v for k,v in price_filter if k == 'discount']
        sql = ' '.join(['select * from price',
            'join brickset on brickset.number = price.set_number',
            ' and '.join(wheres),
            'ORDER BY discount',])
        print sql
        print args
        rows = self.query_db(sql, args)
        return rows

    def query_price_cp(self, set_number ,vendor):
        """query lego current price within one hour"""

        delta = datetime.timedelta(hours=-1)
        now = datetime.datetime.now() + delta
        hour_ago = now.strftime("%Y%m%d%H%M%S")
        sql = """
            SELECT * FROM price
            WHERE datetime>=? AND set_number=? AND vendor=?
            ORDER BY price
        """
        args = (hour_ago, set_number, vendor)
        row = self.query_db(sql, args, one=True)
        return row

    def query_update_log(self,content):
        sql = "select * from update_log where content = ? order by end desc"
        args = (content,)
        row = self.query_db(sql, args, one=True)
        return row

    def append_db(self, table, fields, datas):
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
            self.cx.executemany(sql, args)
        else:
            for data in datas:
                args = ([datas.get(field) for field in fields])
            self.cx.execute(sql, args)
        self.cx.commit()

    def append_prices(self, datas):
        """append price to db"""

        table = 'price'
        fields = ('set_number', 'price', 'discount', 'vendor',
                  'datetime', 'asin', 'item_url', 'title')
        self.append_db(table, fields, datas)

    def append_exrate(self, datas):
        """ append current exrate to db"""

        table = 'exrate'
        fields = ('usd', 'gbp', 'eur', 'cad', 'datetime')
        self.append_db(table, fields, datas)

    def append_update_log(self, datas):
        """write update_log to db"""

        table = 'update_log'
        fields = ('start', 'end', 'content')
        self.append_db(table, fields, datas)

    def calc_disc(self, set_number, CC, amount):
        """
        function:
            calc discount
        usage:
            db = LegoDb()
            db.connect_db()
            print db.calc_disc('60068-1','CNY','500.20')
            db.disconnect_db()
        arg:
            set_number: the set number of lego item(e.g. 8088-1)
            CC:CurrencyCode(e.g. CNY)
            amount: amount of price(e.g. 123.00)
        return:
            discount:type is float, compare with us rrp (e.g. 57.01)
        """
        #check args
        #check set_number
        #check CC
        cc = CC.lower()
        #check amount
        try:
            amount = float(amount)
        except:
            return None

        row = self.query_brickset(True, 'usprice', number=set_number)
        rate = self.query_exrate()
        if row and row['usprice']:
            us_rrp_rmb = float(row['usprice']) * float(rate['usd'])/100
        else:
            return None

        if cc == u'cny':
            rrp_rmb = amount
        else:
            rrp_rmb = amount*float(rate[cc])/100

        disc = round(rrp_rmb/us_rrp_rmb*100, 2)
        return disc

if __name__ == '__main__':
    db = LegoDb()
    db.connect_db()
    #LegoDb().create_view('brickset_number_view')
    #print db.query_brickset_by_set_number('60052-1')
    #print db.query_exrate()
    #db.create_table('exrate')
    print db.calc_disc('60068-1','CNY','500.20')
    #db.query_brickset(True, 'number', number=444)
    #print db.query_brickset(True, number='8088-1')
    #db.query_brickset(True)
    db.disconnect_db()

