# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:54:15 2015

@author: Kristofer

This script converts several datasets created by the team into a json format,
which can then be sued in the D3 library to build other visulazations of the
transportation network.
"""

import pandas as pd
from shapely.geometry import Polygon, Point
import shapefile


aug = pd.read_csv('augmented_stops.csv')
wards = pd.read_csv('wards.csv') #a file containing ward number and name
adj = pd.read_csv('adj_matrix.csv')
shapefileWards = "C:\Users\Kristofer\HubHacks\Shapefiles\Wards\Wards.shp"

"""
It saves time to construct the shape onjects in this way at once.
"""

poly_sf = shapefile.Reader(shapefileWards)
Ward1 = Polygon(poly_sf.shapes()[0].points)
Ward2 = Polygon(poly_sf.shapes()[1].points)
Ward3 = Polygon(poly_sf.shapes()[2].points)
Ward4 = Polygon(poly_sf.shapes()[3].points)
Ward5 = Polygon(poly_sf.shapes()[4].points)
Ward6 = Polygon(poly_sf.shapes()[5].points)
Ward7 = Polygon(poly_sf.shapes()[6].points)
Ward8 = Polygon(poly_sf.shapes()[7].points)
Ward9 = Polygon(poly_sf.shapes()[8].points)
Ward10 = Polygon(poly_sf.shapes()[9].points)
Ward11 = Polygon(poly_sf.shapes()[10].points)
Ward12 = Polygon(poly_sf.shapes()[11].points)
Ward13 = Polygon(poly_sf.shapes()[12].points)
Ward14 = Polygon(poly_sf.shapes()[13].points)
Ward15 = Polygon(poly_sf.shapes()[14].points)
Ward16 = Polygon(poly_sf.shapes()[15].points)
Ward17 = Polygon(poly_sf.shapes()[16].points)
Ward18 = Polygon(poly_sf.shapes()[17].points)
Ward19 = Polygon(poly_sf.shapes()[18].points)
Ward20 = Polygon(poly_sf.shapes()[19].points)
Ward21 = Polygon(poly_sf.shapes()[20].points)
Ward22 = Polygon(poly_sf.shapes()[21].points)

Ward_List = [Ward1,Ward2,Ward3,Ward4,Ward5,Ward6,Ward7,Ward8,Ward9,Ward10,Ward11,
             Ward12,Ward13,Ward14,Ward15,Ward16,Ward17,Ward18,Ward19,Ward20,Ward21,Ward22,]

wards['Lat'] = wards.apply(lambda row: GetLat(Ward_List, row['Ward']),axis = 1)
wards['Lon'] = wards.apply(lambda row: GetLon(Ward_List, row['Ward']),axis = 1)
wards['totalStops'] = wards.Ward.apply(lambda x: aug[aug.Ward == x].stop_id.nunique())
wards['Area'] = wards.apply(lambda row: AppxArea(Ward_List, row['Ward']), axis =1)

def GetLon(WardList, Ward):
    """Returns the centorid Longitude of the Ward - uses a list of Ward Shapely Objects"""
    for i in range(len(WardList)):
        if i == Ward -1: 
            return WardList[i].centroid.coords.xy[1][0]
    
def GetLat(WardList, Ward):
    """Returns the centorid Longitude of the Ward - uses a list of Ward Shapely Objects"""
    for i in range(len(WardList)):
        if i == Ward -1: 
            return WardList[i].centroid.coords.xy[0][0]
            
def TotalStops(augmented_stops, ward):
    """Returns the unique total bus stops in a Ward, from the augmented stops df"""
    return augmented_stops[augmented_stops.Ward == ward].stop_id.nunique()

def AppxArea(WardList,Ward):
    """Returns an approximate area for the Ward. Converting the planar area to
    an unprojected area approximation"""
    for i in range(len(WardList)):
        if i == Ward - 1:
            return WardList[i].area*10000

WardtoJson = wards
AdjtoJson = adj

AdjtoJson.source = AdjtoJson.source.apply(lambda x: (x-1)) #Wards need to be indexed to a zero index to build the network in D3
AdjtoJson.target = AdjtoJson.target.apply(lambda x: (x-1)) #Wards need to be indexed to a zero index to build the network in D3

f=open('file.json', 'w')
f.writelines(["{",'"nodes":' '\n', '  [', '\n'])
for i in range((len(WardtoJson)-1)):
    f.writelines(['    {"Name": "', WardtoJson.iloc[i].Name, '"' , ','
    , '"Area": ',str(WardtoJson.iloc[i].Area), ', '
    , '"Ward": ', str(WardtoJson.iloc[i].Ward), ', '
    , '"totalStops": ', str(WardtoJson.iloc[i].totalStops), ', '
    , '"Longitude": ', str(WardtoJson.iloc[i].Lon), ', '
    , '"Latitude": ', str(WardtoJson.iloc[i].Lat), ', '
    , '"Population": ', str(WardtoJson.iloc[i].Population), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"Name": "', WardtoJson.iloc[len(WardtoJson)-1].Name, '"', ','
    , '"Area": ',str(WardtoJson.iloc[len(WardtoJson)-1].Area), ', '
    , '"Ward": ', str(WardtoJson.iloc[len(WardtoJson)-1].Ward), ', '
    , '"totalStops": ', str(WardtoJson.iloc[len(WardtoJson)-1].totalStops), ', '
    , '"Longitude": ', str(WardtoJson.iloc[len(WardtoJson)-1].Lon), ', '
    , '"Latitude": ', str(WardtoJson.iloc[len(WardtoJson)-1].Lat), ', '
    , '"Population": ', str(WardtoJson.iloc[len(WardtoJson)-1].Population), '}'
    ])
f.write('\n')
f.writelines(['],','\n','"links":[', '\n'])
for j in range(len(adj)-1):
    f.writelines(['    {"source": ', str(AdjtoJson.iloc[j].source), ','
    , '"target": ',str(AdjtoJson.iloc[j].target), ', '
    , '"value": ', str(AdjtoJson.iloc[j].weight), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"source": ', str(AdjtoJson.iloc[len(AdjtoJson)-1].source), ','
    , '"target": ',str(AdjtoJson.iloc[len(AdjtoJson)-1].target), ', '
    , '"value": ', str(AdjtoJson.iloc[len(AdjtoJson)-1].weight), '}'
    ])
f.write('\n')
f.writelines([']','}'])
f.close()