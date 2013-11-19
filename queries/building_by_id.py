#!/usr/bin/env python


# Import the cgi module,json and initialize the database connection
import cgi
import dbconn

# Initialize the FieldStorage object so we can get user input
params = cgi.FieldStorage()

# Run the query, quoting the user input
dbconn.send_query("""
SELECT 
floor,
ST_AsGeoJson(the_geom) AS the_geom 
FROM 
rooms 
WHERE 
building=""" + dbconn.adapt(str(params['building'].value)).getquoted() + """
""") 
