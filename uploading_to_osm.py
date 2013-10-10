import sqlite3 as lite
import sys
from pprint import pprint
import json
import urllib2
import OsmApi

con = None

con = lite.connect('../building_id/dev_db.db')
with con:
    print con
    
    cur = con.cursor()    
    # cur.execute('SELECT * from psuedonumber')
    # rows = cur.fetchall()

    # for row in rows:
    # 	print row

def convert(input): #this converts unicode object to string object in the decoded json file
    if isinstance(input, dict):
        return dict([(convert(key), convert(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

## Getting data from internet
# formhub_request = urllib2.Request('https://formhub.org/nirabpudasaini/forms/fullexposure_form_new/api')
# formhub_response = urllib2.urlopen(formhub_request)
formhub_response = open('data_from_formhub.json')
json_data = json.loads(formhub_response.read())
if(json_data):
	print "got response"
else:
	print "no response"
json_data = convert(json_data)
# pprint(json_data)

##OSMapi
MainApi = OsmApi.OsmApi()
DevApi = OsmApi.OsmApi(api='api06.dev.openstreetmap.org', username = 'amrit_karma', password = 'openstreetmap', changesetauto=True, debug=True)
# dev_capabiliies = DevApi.Capabilities()
# print dev_capabiliies

kll = DevApi.WayGet(4295036827)
print 'kll=',kll
# new_kll = DevApi.WayUpdate(kll)
# new_changeset = DevApi.ChangesetCreate()
# new_changeset.close
# print new_changeset

