import sqlite3 as lite
import sys
from pprint import pprint
import json
import urllib2

con = None

con = lite.connect('../building_id/dev_db.db')
with con:
    print con
    
    cur = con.cursor()    
    # cur.execute('SELECT * from psuedonumber')
    # rows = cur.fetchall()

    # for row in rows:
    # 	print row

## Getting data from internet
# req = urllib2.Request('http://www.voidspace.org.uk')
# response = urllib2.urlopen(req)
# the_page = response.read()
# if(the_page):
# 	print "got response"
# 	# print the_page
# else:
# 	print "no response"

def convert(input):
    if isinstance(input, dict):
        return dict([(convert(key), convert(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

json_data_con=open('data_from_formhub.json')
json_data = json.load(json_data_con)
json_data = convert(json_data[0])
pprint(json_data)
print (json_data['building_id'])

