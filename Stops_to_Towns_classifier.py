# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:55:08 2015

@author: Kristofer
"""
# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Polygon, Point
import shapefile
import pyproj
import csv

wgs84= pyproj.Proj("+init=EPSG:4326")
myProj = pyproj.Proj("+proj=lcc +lat_1=41.71666666666667 +lat_2=42.68333333333333 +lat_0=41 +lon_0=-71.5 +x_0=200000 +y_0=750000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs", preserve_units = True)

def GetTown_fromList(TownDict, Point):
    """Create the Ward_List. Creating the Shapely geometries takes the most
    time. Only do this once the iteration takes no time at all.
    """
    for key, value in TownDict.iteritems():
#            print i
        New_Shape = value #The ith shape in the shapefile
        if New_Shape.contains(Point):
#                print 'point found'
            town = key
#            print town
            return town

"""Data Imports"""
stops = pd.read_csv('C:\Users\Kristofer\HubHacks\GFTS\stops.csv') #Coordinates in WGS84
shapefileTowns = "C:\Users\Kristofer\HubHacks\Shapefiles\Towns\TOWNSSURVEY_POLYM.shp" #Coordinates in NAD83

towns = shapefile.Reader(shapefileTowns)

Town_Dict = {} # create a dictionary of town names and town polygons.

for i in range(towns.numRecords):
    Town_Dict[towns.records()[i][0]] = Polygon(towns.shapes()[i].points)
    
"""Adding rows to the stops csv file""" 
stops['PointWGS84'] = stops.apply(lambda row: Point(row['stop_lon'],row['stop_lat']),axis=1) #Create a Column that contains shapely Point Objects
stops['PointNAD83'] = stops.apply(lambda row: Point(pyproj.transform(wgs84,
                        myProj, row['stop_lon'], row['stop_lat'])),axis=1) #Create a Column that contains shapely Point Objects in NAD83 projection
stops['Town'] = stops.apply(lambda row: GetTown_fromList(Town_Dict, row['PointNAD83']),axis=1)

"""Write the augmented csv file to disk"""

f = open('augmented_stoplist_towns.csv', "wb")
cw = csv.writer(f)
cw.writerow(['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'town']) # header row
for i in range(len(stops)):
    val1, val2, val3, val4, val5 = stops.iloc[i].stop_id, stops.iloc[i].stop_name ,stops.iloc[i].stop_lat,stops.iloc[i].stop_lon,stops.iloc[i].Town
    cw.writerow([val1, val2, val3,val4,val5]) 
f.close()

"""Create dataframe to use in building JSON output by town"""

aug = pd.read_csv('augmented_stoplist_towns.csv') #needed to count the total stops per town

data = {'Town':Town_Dict.keys()}
df = pd.DataFrame(data) #create a df Object with the Town names as the row

def GetLon(TownDict, town):
    """Returns the centorid Longitude of the Ward - uses a dictionary of Ward Shapely Objects"""
    centroid = TownDict[town].centroid.coords.xy
    NAD83lon = centroid[1][0]
    NAD83lat = centroid[0][0]
    WGS84point = pyproj.transform(myProj,wgs84, NAD83lon, NAD83lat)
    return WGS84point[0]
            
def GetLat(TownDict, town):
    """Returns the centorid Longitude of the Ward - uses a dictionary of Ward Shapely Objects"""
    centroid = TownDict[town].centroid.coords.xy
    NAD83lon = centroid[1][0]
    NAD83lat = centroid[0][0]
    WGS84point = pyproj.transform(myProj,wgs84, NAD83lon, NAD83lat)
    return WGS84point[1]
            
def TotalStops(augmented_stops, town):
    """Returns the unique total bus stops in a Town, from the augmented stops df"""
    return augmented_stops[augmented_stops.town == town].stop_id.nunique()

def Pop1980(town_sf, town):
    for i in range(town_sf.numRecords):
        if town_sf.records()[i][0] == town: #select the right town
            return town_sf.records()[i][2]

def Pop1990(town_sf, town):
    for i in range(town_sf.numRecords):
        if town_sf.records()[i][0] == town: #select the right town
            return town_sf.records()[i][3]

def Pop2000(town_sf, town):
    for i in range(town_sf.numRecords):
        if town_sf.records()[i][0] == town: #select the right town
            return town_sf.records()[i][4]

def Pop2010(town_sf, town):
    for i in range(town_sf.numRecords):
        if town_sf.records()[i][0] == town: #select the right town
            return town_sf.records()[i][12]

def Acres(town_sf, town):
    for i in range(town_sf.numRecords):
        if town_sf.records()[i][0] == town: #select the right town
            return town_sf.records()[i][10]
         
df['Lon'] = df.apply(lambda row: GetLon(Town_Dict, row['Town']), axis=1)
df['Lat'] = df.apply(lambda row: GetLat(Town_Dict, row['Town']), axis=1)
df['totalStops'] = df.Town.apply(lambda x: aug[aug.town == x].stop_id.nunique())
df=df[df.totalStops!=0] #filters the dataframe to only towns with at least one stop.
print 'pop start'
df['Pop1980'] = df.Town.apply(lambda x: Pop1980(towns,x)) #towns is a shapefile Reader instance of the MASS Towns shapefile
print '1980'
df['Pop1990'] = df.Town.apply(lambda x: Pop1990(towns,x)) 
print '1990'
df['Pop2000'] = df.Town.apply(lambda x: Pop2000(towns,x)) 
print '2000'
df['Pop2010'] = df.Town.apply(lambda x: Pop2010(towns,x)) 
print '2010'
df['Acres'] = df.Town.apply(lambda x: Acres(towns,x)) 

df.to_csv('towns_JSON_constructor.csv') 
#This data frame and the adjacency matrix from the mbta_town_constructor are required to create the JSON file format for viewing in D3


