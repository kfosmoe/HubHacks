# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:42:39 2015

@author: Kristofer
"""

import csv
import pandas as pd
import geopandas as gp
import shapefile
from shapely.geometry import Polygon, Point
import pyproj

NAD83= pyproj.Proj("+init=EPSG:2249", preserve_units = True)
wgs84= pyproj.Proj("+init=EPSG:4326")

folder = "C:/Users/Kristofer/HubHacks/geo/"

df = pd.read_csv('route_summary.csv') #Run Keeper route summary provied csv file
df['geometry'] = df.routeid.apply(lambda x: gp.GeoSeries.from_file(folder+x+'.geojson')) #creates a linestring for each routeid in the summary file
df['start_point'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis =1)

def GetNeighborhood(Dict, Point):
    """Returns the neighborhood containing the Point, where the key is the name of the neighborhood"""
    for key in Dict:
        if Dict[key].contains(Point):
            return key

neighborhoods = shapefile.Reader("C:/Users/Kristofer/HubHacks/Shapefiles/boston_neighborhood/Bos_neighborhoods_new.shp")

Neighborhood_Dict = {}

for i in range(neighborhoods.numRecords):
    point_list = neighborhoods.shapes()[i].points #a list of points in NAD83 CRS
    transformed_points = []    
    for j in range(len(point_list)):
        x=point_list[j][0]
        y=point_list[j][1]
        transformed_x = pyproj.transform(NAD83,wgs84,x,y)[0]
        transformed_y = pyproj.transform(NAD83,wgs84,x,y)[1] #pyproj transform returns a tuple
        transformed_point = [transformed_x, transformed_y] #shapely objects need to be a list of lists
        transformed_points.append(transformed_point)
    Neighborhood_Dict[neighborhoods.records()[i][1]] = Polygon(transformed_points)

df['start_neighborhood'] = df.start_point.apply(lambda x: GetNeighborhood(Neighborhood_Dict,x))

run_conn = {}
for i in range(len(df)):
    route = df.iloc[i].geometry #shapely linestring object for the run route
    trip_id = df.iloc[i].routeid
    for key in Neighborhood_Dict.keys():
        if Neighborhood_Dict[key].intersects(route): #the route-line and the geometry intersect
            if trip_id not in run_conn:
                run_conn[trip_id] = [key] #add the new route to the run_conn dictionary
            elif key not in run_conn[trip_id]: #check if the geometry is already listed on that route
                run_conn[trip_id].append(key)

# create edges between wards connected in the same route
adj_hash = {}
for key in run_conn.iteritems():  
    for i in xrange(len(key[1]) - 1):
        for j in xrange(i + 1, len(key[1])):
            if key[1][i] < key[1][j]:
                tuple_key = (key[1][i], key[1][j])
            else:
                tuple_key = (key[1][j], key[1][i])
            if tuple_key not in adj_hash:
            	adj_hash[tuple_key] = 1
            else:
            	adj_hash[tuple_key] += 1

# write the results to csv
f= open('adj_run_list.csv', 'wb')
cw = csv.writer(f)
cw.writerow(['source', 'target', 'weight', 'type'])  # label the outputted .
for val in adj_hash.iteritems():
    val1, val2, val3 = val[0][0], val[0][1], val[1]
    cw.writerow([val1, val2, val3, 'undirected'])
f.close()

df.to_csv('run_keeper_data.csv')