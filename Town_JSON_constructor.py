# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:22:56 2015

@author: Kristofer
"""

import pandas as pd

links = pd.read_csv('adj_town_list_output.csv')
nodes = pd.read_csv('towns_JSON_constructor.csv')

#Create an integer based dictionary for the town names
Town_int = {}
for i in range(len(nodes)):
    Town_int[nodes.iloc[i].Town] = i

links['int_source'] = links.source.apply(lambda x: Town_int[x])
links['int_target'] = links.target.apply(lambda x: Town_int[x])


"""Create JSON File from imported dataframes"""

f=open('town_file.json', 'w')
f.writelines(["{",'"nodes":' '\n', '  [', '\n'])
for i in range((len(nodes)-1)):
    f.writelines(['    {"Name": "', nodes.iloc[i].Town, '"' , ','
    , '"Acres": ',str(nodes.iloc[i].Acres), ', '
    , '"totalStops": ', str(nodes.iloc[i].totalStops), ', '
    , '"Longitude": ', str(nodes.iloc[i].Lon), ', '
    , '"Latitude": ', str(nodes.iloc[i].Lat), ', '
    , '"Population_1980": ', str(nodes.iloc[i].Pop1980), ','
    , '"Population_1990": ', str(nodes.iloc[i].Pop1990), ','
    , '"Population_2000": ', str(nodes.iloc[i].Pop2000), ','
    , '"Population_2010": ', str(nodes.iloc[i].Pop2010), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"Name": "', nodes.iloc[len(nodes)-1].Town, '"', ','
    , '"Acres": ',str(nodes.iloc[len(nodes)-1].Acres), ', '
    , '"totalStops": ', str(nodes.iloc[len(nodes)-1].totalStops), ', '
    , '"Longitude": ', str(nodes.iloc[len(nodes)-1].Lon), ', '
    , '"Latitude": ', str(nodes.iloc[len(nodes)-1].Lat), ', '
    , '"Population_1980": ', str(nodes.iloc[i].Pop1980), ','
    , '"Population_1990": ', str(nodes.iloc[i].Pop1990), ','
    , '"Population_2000": ', str(nodes.iloc[i].Pop2000), ','
    , '"Population_2010": ', str(nodes.iloc[len(nodes)-1].Pop2010), '}'
    ])
f.write('\n')
f.writelines(['],','\n','"links":[', '\n'])
for j in range(len(links)-1):
    f.writelines(['    {"source": ', str(links.iloc[j].int_source), ','
    , '"target": ',str(links.iloc[j].int_target), ', '
    , '"value": ', str(links.iloc[j].weight), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"source": ', str(links.iloc[len(links)-1].int_source), ','
    , '"target": ',str(links.iloc[len(links)-1].int_target), ', '
    , '"value": ', str(links.iloc[len(links)-1].weight), '}'
    ])
f.write('\n')
f.writelines([']','}'])
f.close()