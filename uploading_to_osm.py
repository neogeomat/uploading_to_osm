import sqlite3 as lite
import sys
from pprint import pprint
import json
import urllib2
import OsmApi

print 'python version=',sys.version
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
print type(json_data)

##OSMapi
MainApi = OsmApi.OsmApi()
DevApi = OsmApi.OsmApi(api='api06.dev.openstreetmap.org', passwordfile = 'devpassword', changesetauto=True, debug=True)
# dev_capabiliies = DevApi.Capabilities()
# print dev_capabiliies

# old_data = convert(MainApi.WayFull(json_data[1]['building_id']))
# print 'old_data full'
old_data = convert(MainApi.WayGet(json_data[1]['building_id']))
pprint(old_data)
print 'old_data'
# pprint(MainApi.WayGet(json_data[1]['building_id']))


























# for element in old_data:
    # pprint(element)
    # if(element['type']=='node'):
    #     print 'node'
    #     new_node = {'lat':element['data']['lat'],'lon':element['data']['lon'],'tag':element['data']['tag']}
    #     pprint(new_node)
    #     node_create = convert(DevApi.NodeCreate(new_node))
    #     print 'node_create',node_create
    #     print new_data['nd']
    #     print new_data['nd'].append(0)
    # elif(element['type']=='way'):
    #     print 'way'
    #     new_data['tag'] = element['data']['tag']
        # way_create = DevApi.WayCreate(new_way)

# for building in json_data:
#     # print building['building_id']
#     if(len(building['building_id'])== 9):
#         osmid = building['building_id']
#         print 'osmid',osmid
        # old_data = MainApi.WayGet(building['building_id'])
        # pprint(old_data)
        # for row in building:
            # old_data[row] = building[row]
        # DevApi.WayCreate(old_data)
