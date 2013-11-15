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
floor,
ST_AsGeoJson(the_geom) AS the_geom 
FROM 
rooms 
WHERE 
building=""" + dbconn.adapt(str(params['building'].value)).getquoted() + """
""") 

output = {
        'type' : 'FeatureCollection',
        'features' : []
}

for row in dbconn.cur:
    # Make a single feature
    one = {
            'type' : 'Feature',
            'geometry' : json.loads(row['the_geom']),
            'properties' : {}
    }

    # Apply its properties
    for k in row.keys():
        if k != 'the_geom':
            one['properties'][k] = row[k]

    # Stick it in our collection
    output['features'].append(one)

# Encode resulting object as json
print json.dumps(output)
