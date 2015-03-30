import csv

# create dictionary w/ stop_id as key and ward as value
with open('augmented_stops.csv', 'rU') as filename:
    reader = csv.reader(filename, delimiter = ",")
    reader.next()   # skip header line
    
    stop_ward = {}
    for line in reader:
        if line[11] != '':
            stop_ward[line[0]] = line[11]
    
# create dictionary w/ trip_id as key and list of wards trip passes through as value
with open('stop_times.txt', 'rU') as filename1:
    reader = csv.reader(filename1, delimiter = ",")
    reader.next()   # skip header line

    ward_conn = {}
    for line in reader:
    	try:
            ward = stop_ward[line[3]]
            if line[0] not in ward_conn:
                ward_conn[line[0]] = [ward]
            elif ward not in ward_conn[line[0]]:
                ward_conn[line[0]].append(ward)
        except:
        	KeyError

# create edges between wards connected in the same trip
adj_hash = {}
for key in ward_conn.iteritems():  
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
cw = csv.writer(open('adj_list_output.csv', "wb"))
cw.writerow(['source', 'target', 'weight', 'type'])  # label the outputted .
for val in adj_hash.iteritems():
    val1, val2, val3 = val[0][0], val[0][1], val[1]
    cw.writerow([val1, val2, val3, 'undirected']) 






