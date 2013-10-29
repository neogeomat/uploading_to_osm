import sqlite3 as lite
import sys
from pprint import pprint
import json
import urllib2
import OsmApi
from mylib import convert
import random

print 'python version=',sys.version
overpass_api = "http://www.overpass-api.de/data"
con = None
con = lite.connect('../building_id/dev_db.db')
# with con:
#     print con
    
#     cur = con.cursor()    
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
# print type(json_data)

##OSMapi
MainApi = OsmApi.OsmApi(passwordfile = 'mainpassword')
DevApi = OsmApi.OsmApi(api='api06.dev.openstreetmap.org', passwordfile = 'devpassword',debug=True)
# dev_capabiliies = DevApi.Capabilities()
# print dev_capabiliies

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

        elif(len(building['building_id'])<=4):  #for pseudonumber connect to db and find number
            with con:
                cur = con.cursor()    
                cur.execute('SELECT osmid from psuedonumber where district=\"',building['district'],'\" AND vdc=\"',building['vdc'],'\" AND ward=\"',building['ward'],'\" AND new_id=\"',building_id,'\"')
                osmid = cur.fetchone()
        else:
            pass

    elif(building['new_building'] == "new_building_false"):
        if(building['area_id']):
            building_id = [building['area_id'], building['building_id']]

    #after id is determined
    if(osm_id):
        old_data = convert(MainApi.WayFull(osm_id)

        if(not old_data['data']['tag']['building:structure']):
            
            #preserving old data
            new_data = {'tag':old_data['data']['tag']}
            
            #building ownership
            if(building["building_own"] == "building_own_rent"):
                new_data['tag']['building:ownership'] = "rent"
            else:
                new_data['tag']['building:ownership'] = "self"

            # building structural system
            if(building["building_struct"] == "building_struct_erc"):
                new_data['tag']["building:structure"] = "engineered_reinforced_concrete"
            elif(building["building_struct"] == "building_struct_nrc"):
                new_data['tag']["building:structure"] = "non_engineered_reinforced_concrete"
            elif(building["building_struct"] == "building_struct_sc"):
                new_data['tag']["building:structure"] = "load_bearing_stone_wall_in_cement_mortar"
            elif(building["building_struct"] == "building_struct_bls"):
                new_data['tag']["building:structure"] = "load_bearing_brick_wall_in_lime_surkhi_mortar"
            elif(building["building_struct"] == "building_struct_bc"):
                new_data['tag']["building:structure"] = "load_bearing_brick_wall_in_cement_mortar"
            elif(building["building_struct"] == "building_struct_bm"):
                new_data['tag']["building:structure"] = "load_bearing_brick_wall_in_mud_mortar"
            elif(building["building_struct"] == "building_struct_dsm"):
                new_data['tag']["building:structure"] = "load_bearing_dry_stone_wall"
            elif(building["building_struct"] == "building_struct_sm"):
                new_data['tag']["building:structure"] = "load_bearing_stone_wall_in_mud_mortar"
            elif(building["building_struct"] == "building_struct_ad"):
                new_data['tag']["building:structure"] = "adobe"

            # no of stories
            if(building["building_stories"]):
                new_data['tag']['building:levels'] = building["building_stories"]

            # building use
            if(building["building_use"] == "building_use_res"):
                new_data['tag']['building:use'] = 'residential'
            elif(building["building_use"] == "building_use_edu"):
                new_data['tag']['building:use'] = 'education'
            elif(building["building_use"] == "building_use_hel"):
                new_data['tag']['building:use'] = 'health'
            elif(building["building_use"] == "building_use_com"):
                new_data['tag']['building:use'] = 'commercial'
            elif(building["building_use"] == "building_use_res"):
                new_data['tag']['building:use'] = 'residential'

            # floor material type
            if(building["building_flt"] == "building_flt_rig"):
                new_data['tag']['floor:material:type'] = 'rigid'
            elif(building["building_flt"] == "building_flt_fle"):
                new_data['tag']['floor:material:type'] = 'flexible'

            # roof material type
            if(building["building_rft"] == "building_rft_rig"):
                new_data['tag']['roof:material:type'] = 'rigid'
            elif(building["building_rft"] == "building_rft_fle"):
                new_data['tag']['roof:material:type'] = 'flexible'

            # building attachment
            if(building["building_attach"] == "building_attach_true"):
                new_data['tag']['building:adjacency'] = "yes"
            elif(building["building_attach"] == "building_attach_false"):
                new_data['tag']['building:adjacency'] = "no"

            # shape in plan
            if(building["building_shape_plan"] == "building_shape_plan_r"):
                new_data['tag']['shape:plan'] = "regular"
            elif(building["building_shape_plan"] == "building_shape_plan_r"):
                new_data['tag']['shape:plan'] = "irregular"

            # shape in elevation
            if(building["building_shape_elev"] == "building_shape_elev_r"):
                new_data['tag']['shape:elevation'] = "regular"
            elif(building["building_shape_elev"] == "building_shape_elev_ir"):
                new_data['tag']['shape:elevation'] = "irregular"
            elif(building["building_shape_elev"] == "building_shape_elev_nt"):
                new_data['tag']['shape:elevation'] = "narrow_tall"
            elif(building["building_shape_elev"] == "building_shape_elev_ntir"):
                new_data['tag']['shape:elevation'] = "narrow_tall_irregular"

            # visible physical condition
            if(building["building:condition"] == "building_condition_poor"):
                new_data['tag']['physical_condition'] = "poor"
            elif(building["building:condition"] == "building_condition_avg"):
                new_data['tag']['physical_condition'] = "average"
            elif(building["building:condition"] == "building_condition_good"):
                new_data['tag']['physical_condition'] = "good"

            # building overhang
            if(building["building_overhang"]=="building_overhang_false"):
                new_data['tag']['building:overhang'] = 'no'
            elif(building["building_overhang"]=="building_overhang_true"):
                new_data['tag']['building:overhang'] = 'yes'

            # building soft storey
            if(building["building_softstor"]=="building_softstor_false"):
                new_data['tag']['building:soft_storey'] = 'no'
            elif(building["building_softstor"]=="building_softstor_true"):
                new_data['tag']['building:soft_storey'] = 'yes'

            # building gable wall
            if(building["building_gable"]=="building_gable_false"):
                new_data['tag']['building:gable_wall'] = 'no'
            elif(building["building_gable"]=="building_gable_true"):
                new_data['tag']['building:gable_wall'] = 'yes'

        else:
            print "Data exists for way",osmid

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
