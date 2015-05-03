
import sqlite3

persons = [
    ("Hugo", "Boss"),
    ("Calvin", "Klein")
    ]
con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row

cur = con.cursor()

# Create the table
con.execute("create table person(firstname, lastname)")

# Fill the table
con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)
con.commit()

cur.execute("select 'John' as name, 42 as age")
for row in cur:
    print row, row.keys(), type(row)
    assert row[0] == row["name"]
    assert row["name"] == row["nAmE"]
    assert row[1] == row["age"]
    assert row[1] == row["AgE"]

cur.execute("select * from person")
for row in cur:
    print row, row.keys(), type(row)


DATABASE = '/home/dormouse/project/legohole/testdata/test.db'

cx = sqlite3.connect(DATABASE)

def query_db(sql, args=(), one=False):
    cur = cx.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    print cur.description
    return (rv[0] if rv else None) if one else rv

print query_db('select * from price')[0]


