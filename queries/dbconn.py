#!/usr/bin/env python

import psycopg2
import psycopg2.extras
from psycopg2.extensions import adapt
import ConfigParser
import simplejson as json

config = ConfigParser.ConfigParser()
config.readfp(open('dbconn.cfg'))

try:
    conn = psycopg2.connect(host = config.get('auth','host'), port = config.get('auth','port'), database = config.get('auth','dbname'), user = config.get('auth','user'), password = config.get('auth','pass'))

    # Create a server-side cursor so we don't end up with all records in memory at once
    # http://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL 
    cur = conn.cursor('dbconn', cursor_factory=psycopg2.extras.DictCursor)
except Exception as e:
    print "Unable to connect to the database"
    print e
    exit()



# Send the results of a query to the browser as geojson
def send_geojson(q):

    cur.execute(q)

    # Build an empty GeoJSON FeatureCollection object, then fill it from the database results
    output = {
            'type' : 'FeatureCollection',
            'features' : []
    }

    for row in cur:
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


    # First we have to print some headers
    # Followed by two blank lines. That's how the browser knows the headers are all done
    print "Content-Type: application/json; charset=utf-8"
    print

    # Encode resulting object as json
    print json.dumps(output)
