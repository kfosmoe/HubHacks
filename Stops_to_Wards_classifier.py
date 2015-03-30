# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:20:03 2015

@author: Kristofer
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:41:53 2015

@author: Kristofer
"""
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
import shapefile

def GetWard_fromList(WardList, Point):
    """Create the Ward_List. Creating the Shapely geometries takes the most
    time. Only do this once the iteration takes no time at all.
    """

    if Point.y >= 42.39693883012769:
#        print 'north'
        return None# the point is north of Boston
    elif Point.y <= 42.22761808904161:
#        print 'south'
        return None # the point is south of Boston
    elif Point.x <= -71.19169875610878:
#        print 'west'
        return None #the point is west of Boston
    elif Point.x >= -70.98625643397861:
#        print 'east' # the Point is east of Boston
        return None
    else: #check the polygons for the ward and precint
        for i in xrange(len(WardList)):
#            print i
            New_Shape = WardList[i] #The ith shape in the shapefile
            if New_Shape.contains(Point):
#                print 'point found'
                ward = i + 1
#                print ward
                return ward

stops = pd.read_csv('C:\Users\Kristofer\HubHacks\GFTS\stops.csv')
shapefilePrecincts = "C:\Users\Kristofer\HubHacks\Precincts.shp"
shapefileWards = "C:\Users\Kristofer\HubHacks\Shapefiles\Wards\Wards.shp"
shapefileUrban = "C:\Users\Kristofer\Hubhacks\Shapefiles\UrbanBoundaries\UrbanBoundary2010.shp"

stops['Point'] = stops.apply(lambda row: Point(row['stop_lon'],row['stop_lat']),axis=1) #Create a Column that contains shapely Point Objects
#stop_times = pd.read_csv('C:\Users\Kristofer\HubHacks\GFTS\stop_times.txt')

"""Getting the bounding box for Boston
poly_sf = shapefile.Reader(shapefileWards)
Ward1 = Polygon(poly_sf.shapes()[0].points) #North and East Points
Ward20 = Polygon(poly_sf.shapes()[19].points) #West Point
Ward18 = Polygon(poly_sf.shapes()[17].points) #South point
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

#stops['Ward'] = stops.apply(lambda row: GetWard_fromList(Ward_List, row['Point']),axis=1)

"""Make a dictionary of routes: stop_ids"""
#d = {} 
#
#for i in range(len(stop_times)):
#    try:
#        d[stop_times.trip_id[i]].append(stop_times.stop_id[i])
#    except KeyError:
#        d[stop_times.trip_id[i]] = [stop_times.stop_id[i]]

def GetWard(shapefileName, Point):
    """shapefileName is the shapefile that contains the wards in Boston.
    Point is a shapely Point object.
    """
    polygons_sf = shapefile.Reader(shapefileName)
    
    if Point.y >= 42.39693883012769:
        print 'north'
        return None# the point is north of Boston
    elif Point.y <= 42.22761808904161:
        print 'south'
        return None # the point is south of Boston
    elif Point.x <= -71.19169875610878:
        print 'west'
        return None #the point is west of Boston
    elif Point.x >= -70.98625643397861:
        print 'east' # the Point is east of Boston
    else: #check the polygons for the ward and precint
        for i in xrange(polygons_sf.numRecords):
#            print i
            New_Shape = polygons_sf.shapes()[i] #The ith shape in the shapefile
            New_Polygon = Polygon(New_Shape.points) #convert the points into shapely polygon
            if New_Polygon.contains(Point):
#                print 'point found'
                records = polygons_sf.records()[i] #The attribute table for the ith record
                ward = records[1]
                ward_prec = records[2]
#                print (ward,ward_prec)
                return ward

aug = pd.read_csv('augmented_stops.csv')
wards = pd.read_csv('wards.csv') #a file containing ward number and name
adj = pd.read_csv('adj_matrix.csv')

wards['Lat'] = wards.apply(lambda row: GetLat(Ward_List, row['Ward']),axis = 1)
wards['Lon'] = wards.apply(lambda row: GetLon(Ward_List, row['Ward']),axis = 1)
wards['totalStops'] = wards.Ward.apply(lambda x: aug[aug.Ward == x].stop_id.nunique())
wards['Area'] = wards.apply(lambda row: AppxArea(Ward_List, row['Ward']), axis =1)