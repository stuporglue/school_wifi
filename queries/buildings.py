#!/usr/bin/env python

# First we have to print some headers
# Followed by two blank lines. That's how the browser knows the headers are all done
print "Content-Type: application/json; charset=utf-8"
print

# Import the cgi module,json and initialize the database connection
import cgi
import dbconn
import json

# Initialize the FieldStorage object so we can get user input
params = cgi.FieldStorage()


dbconn.cur.execute("""
SELECT 
building_n,
ST_AsGeoJson(the_geom) AS the_geom 
FROM 
buildings
""") 

output = {
        'type' : 'FeatureCollection',
        'features' : []
}

for row in dbconn.cur:
    one = {
            'type' : 'Feature',
            'geometry' : json.loads(row['the_geom']),
            'properties' :  {}
    }

    for k in row.keys():
        if k != 'the_geom':
            one['properties'][k] = row[k]

    output['features'].append(one)

# Encode resulting object as json
print json.dumps(output)
