# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:28:41 2015

@author: Kristofer
"""

import pandas as pd
import csv

permits = pd.read_csv('Issued_Permits_ALL_TYPES.csv')

contractors = permits[permits.Is_Contractor == 'Y']

# create dictionary w/ Parcel_ID as key and list of contractors who worked on it
contractor_conn = {}
for i in range(len(contractors)):
    try:
          contractor = contractors.APPLICANT[i]
          parcel = contractors.Parcel_ID[i]
          if parcel not in contractor_conn:
              contractor_conn[parcel] = [contractor]
          elif contractor not in contractor_conn[parcel]:
              contractor_conn[parcel].append(contractor)
    except:
        KeyError
        
# create edges between contractors at the same Parcel_ID
adj_hash = {}
for key in contractor_conn.iteritems():  
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

# write the results of the adj_hash to csv
f= open('contractor_output.csv', 'wb')
cw = csv.writer(f)
cw.writerow(['source', 'target', 'weight', 'type'])  # label the output
for val in adj_hash.iteritems():
    val1, val2, val3 = val[0][0], val[0][1], val[1]
    cw.writerow([val1, val2, val3, 'undirected'])
f.close()

links = pd.read_csv('contractor_output.csv')

#Create an integer based dictionary for the contractor names
contractor_array = contractors.APPLICANT.unique()
contract_int = {}
for i in range(len(contractor_array)):
    contract_int[contractor_array[i]] = i

links['int_source'] = links.source.apply(lambda x: contract_int[x])
links['int_target'] = links.target.apply(lambda x: contract_int[x])

strong_links = links[links.weight>2]

strong_contractor_array = []
for i in range(len(strong_links)):
    if strong_links.iloc[i].source not in strong_contractor_array:
        strong_contractor_array.append(strong_links.iloc[i].source)
for i in range(len(strong_links)):
    if strong_links.iloc[i].target not in strong_contractor_array:
        strong_contractor_array.append(strong_links.iloc[i].target)

strong_contract_dict ={}
for i in range(len(strong_contractor_array)):
    strong_contract_dict[strong_contractor_array[i]] = i
    
strong_links['int_source'] = strong_links.source.apply(lambda x: strong_contract_dict[x])
strong_links['int_target'] = strong_links.target.apply(lambda x: strong_contract_dict[x])

"""Writing to JSON file format"""

f=open('strong_contractor_file.json', 'w')
f.writelines(["{",'"nodes":' '\n', '  [', '\n'])
for i in range((len(strong_contractor_array)-1)):
    f.writelines(['    {"Name": "', str(strong_contractor_array[i]), '"' , '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"Name": "', str(strong_contractor_array[len(strong_contractor_array)-1]), '"', '}'
    ])
f.write('\n')
f.writelines(['],','\n','"links":[', '\n'])
for j in range(len(strong_links)-1):
    f.writelines(['    {"source": ', str(strong_links.iloc[j].int_source), ','
    , '"target": ',str(strong_links.iloc[j].int_target), ', '
    , '"value": ', str(strong_links.iloc[j].weight), '}'
    ])
    f.write(',')
    f.write('\n')
f.writelines(['    {"source": ', str(strong_links.iloc[len(strong_links)-1].int_source), ','
    , '"target": ',str(strong_links.iloc[len(strong_links)-1].int_target), ', '
    , '"value": ', str(strong_links.iloc[len(strong_links)-1].weight), '}'
    ])
f.write('\n')
f.writelines([']','}'])
f.close()
#
#f=open('contractor_file.json', 'w')
#f.writelines(["{",'"nodes":' '\n', '  [', '\n'])
#for i in range((len(contractor_array)-1)):
#    f.writelines(['    {"Name": "', str(contractor_array[i]), '"' , '}'
#    ])
#    f.write(',')
#    f.write('\n')
#f.writelines(['    {"Name": "', str(contractor_array[len(contractor_array)-1]), '"', '}'
#    ])
#f.write('\n')
#f.writelines(['],','\n','"links":[', '\n'])
#for j in range(len(links)-1):
#    f.writelines(['    {"source": ', str(links.iloc[j].int_source), ','
#    , '"target": ',str(links.iloc[j].int_target), ', '
#    , '"value": ', str(links.iloc[j].weight), '}'
#    ])
#    f.write(',')
#    f.write('\n')
#f.writelines(['    {"source": ', str(links.iloc[len(links)-1].int_source), ','
#    , '"target": ',str(links.iloc[len(links)-1].int_target), ', '
#    , '"value": ', str(links.iloc[len(links)-1].weight), '}'
#    ])
#f.write('\n')
#f.writelines([']','}'])
#f.close()
