#!/usr/bin/env python


# Import the cgi module,json and initialize the database connection
import cgi
import dbconn

def roomJacks():

    # Initialize the FieldStorage object so we can get user input
    params = cgi.FieldStorage()

    # Run the query, quoting the user input
    dbconn.send_query("""
            SELECT
			ST_AsGeoJSON(st_centroid(rooms.the_geom)) AS the_geom,
			split_part(jack,'-',3) AS floor,
			split_part(jack,'-',4) AS room
			FROM access_points,rooms WHERE 
			split_part(jack,'-',2)=""" +
			dbconn.adapt(str(params['building'].value)).getquoted() + """
			AND
			split_part(rooms.room_id, '-', 2)=""" +
			dbconn.adapt(str(params['building'].value)).getquoted() + """
			AND
			lpad(split_part(rooms.room_id, '-', 4),5,'0')=split_part(jack,'-',4)
    """) 

roomJacks()
