# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 08:37:22 2015

@author: Kristofer
"""

import pandas as pd

links = pd.read_csv('adj_run_list.csv')
nodes = pd.read_csv('neighborhood_census.csv')
routes = pd.read_csv('run_keeper_data.csv')

nodes.fillna(value=5) #we want to keep some values even if the data is empty for viewing
nodes=nodes[nodes.Name.notnull()] #to remove errors in parsing csv file with null names

#Create an integer based dictionary for the town names
run_int = {}
for i in range(len(nodes)):
    run_int[nodes.iloc[i].Name] = i

links['int_source'] = links.source.apply(lambda x: run_int[x])
links['int_target'] = links.target.apply(lambda x: run_int[x])

nodes['num_starting_routes'] = nodes.Name.apply(lambda x: routes[routes.start_neighborhood == x].routeid.count())

links = links[links.weight>100]

"""Create JSON File from imported dataframes"""
f=open('run_keeper_stronglinks.json', 'w')
f.writelines(["{",'"nodes":' '\n', '  [', '\n'])
for i in range((len(nodes)-1)):
    f.writelines(['    {"Name": "', nodes.iloc[i].Name, '"' , ','
    , '"Population": ',str(nodes.iloc[i].Population), ', '
    , '"totalrouteStarts": ', str(nodes.iloc[i]['num_starting_routes']), ', '
    , '"Males": ', str(nodes.iloc[i].Male_Population), ', '
    , '"Females": ', str(nodes.iloc[i].Female_Population), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"Name": "', nodes.iloc[len(nodes)-1].Name, '"' , ','
    , '"Population": ',str(nodes.iloc[len(nodes)-1].Population), ', '
    , '"totalrouteStarts": ', str(nodes.iloc[len(nodes)-1]['num_starting_routes']), ', '
    , '"Males": ', str(nodes.iloc[len(nodes)-1].Male_Population), ', '
    , '"Females": ', str(nodes.iloc[len(nodes)-1].Female_Population), '}'
    ])
f.write('\n')
f.writelines(['],','\n','"links":[', '\n'])
for j in range(len(links)-1):
    f.writelines(['    {"source": ', str(links.iloc[j].int_source), ','
    , '"target": ',str(links.iloc[j].int_target), ', '
    , '"value": ', str(links.iloc[j].weight/100), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"source": ', str(links.iloc[len(links)-1].int_source), ','
    , '"target": ',str(links.iloc[len(links)-1].int_target), ', '
    , '"value": ', str(links.iloc[len(links)-1].weight/100), '}'
    ])
f.write('\n')
f.writelines([']','}'])
f.close()