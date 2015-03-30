# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:06:36 2015

@author: Kristofer
"""
import csv

# create dictionary w/ stop_id as key and town as value
with open('augmented_stoplist_towns.csv', 'rU') as filename:
    reader = csv.reader(filename, delimiter = ",")
    reader.next()   # skip header line
    
    stop_town = {}
    for line in reader:
        if line[4] != '': #line[4] is the value of the town name
            stop_town[line[0]] = line[4]
    
# create dictionary w/ trip_id as key and list of wards trip passes through as value
with open('stop_times.txt', 'rU') as filename1:
    reader = csv.reader(filename1, delimiter = ",")
    reader.next()   # skip header line

    town_conn = {}
    for line in reader:
    	try:
            town = stop_town[line[3]] #line[3] is the stop_id
            if line[0] not in town_conn: #line[0] is trip_id
                town_conn[line[0]] = [town] #trip_id = town
            elif town not in town_conn[line[0]]:
                town_conn[line[0]].append(town)
        except:
        	KeyError

# create edges between wards connected in the same trip
adj_hash = {}
for key in town_conn.iteritems():  
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
f= open('adj_town_list_output.csv', 'wb')
cw = csv.writer(f)
cw.writerow(['source', 'target', 'weight', 'type'])  # label the outputted .
for val in adj_hash.iteritems():
    val1, val2, val3 = val[0][0], val[0][1], val[1]
    cw.writerow([val1, val2, val3, 'undirected'])
f.close()
