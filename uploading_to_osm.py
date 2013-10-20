import sqlite3 as lite
import sys
from pprint import pprint
import json
import urllib2
import OsmApi
from mylib import convert
import random

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

## Getting data from internet
# formhub_request = urllib2.Request('https://formhub.org/nirabpudasaini/forms/fullexposure_form_new/api')
# formhub_response = urllib2.urlopen(formhub_request)
formhub_response = open('data_from_formhub_10.json')
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
DevApi = OsmApi.OsmApi(api='api06.dev.openstreetmap.org', passwordfile = 'devpassword',debug=True)
# dev_capabiliies = DevApi.Capabilities()
# print dev_capabiliies

# old_data = convert(MainApi.WayFull(json_data[1]['building_id']))
# print 'old_data full'

##data entry
DevApi.ChangesetCreate({'comment':u'full exposure survey','source':u'KathmanduLivingKLabs'})
i=0
for building in json_data:
    # pprint(building)
    print i
    i+=1
    osm_id = None
    ##if building exists query database and find out its id
    if(building['new_building']=="new_building_true"):  #
        building_id = building['building_id']
        if(len(building['building_id'])==9):    #if real osmid is used
            osm_id = building_id
        elif(len(building['building_id'])<=4):  #for pseudonumber connect to db asd find number
            with con:
                cur = con.cursor()    
                cur.execute('SELECT osmid from psuedonumber where district=\"',building['district'],'\" AND vdc=\"',building['vdc'],'\" AND ward=\"',building['ward'],'\" AND new_id=\"',building_id,'\"')
                osmid = cur.fetchone()
        else:
            print ""
    #after id is determined
    if(osm_id):
        osm_id   = building['building_id'])
        old_data = convert(MainApi.WayGet(osm_id)
        new_data = {'tag':old_data['tag'],'lat':(27.7+random.random()*0.01),'lon':(85.3+random.random()*0.01)} #preserving old data
        if(building["building_overhang"]=="building_overhang_false"):
            new_data['tag']['building:overhang'] = 'no'
        elif(building["building_overhang"]=="building_overhang_true"):
            new_data['tag']['building:overhang'] = 'yes'
        print DevApi.NodeCreate(new_data)
    #
DevApi.ChangesetClose()




























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
