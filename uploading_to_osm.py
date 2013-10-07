import sqlite3 as lite
import sys

con = None

con = lite.connect('../building_id/table_ko_name.db')
with con:
    print con
    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    
    data = cur.fetchone()
    
    print "SQLite version: %s" % data