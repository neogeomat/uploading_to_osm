import sqlite3 as lite
import sys

con = None

con = lite.connect('../building_id/dev_db.db')
with con:
    print con
    
    cur = con.cursor()    
    cur.execute('SELECT * from psuedonumber')
    rows = cur.fetchall()

    for row in rows:
    	print row