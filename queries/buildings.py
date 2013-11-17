#!/usr/bin/env python

# Import the json and initialize the database connection
import dbconn

# Initialize the FieldStorage object so we can get user input

dbconn.send_geojson("""
SELECT 
building_n,
ST_AsGeoJson(the_geom) AS the_geom 
FROM 
buildings
""") 
