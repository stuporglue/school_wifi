#!/usr/bin/env python


# Import the cgi module,json and initialize the database connection
import cgi
import dbconn

def jbybid():

    # Initialize the FieldStorage object so we can get user input
    params = cgi.FieldStorage()

    # Run the query, quoting the user input
    con = dbconn.run_query("""
            SELECT 
            count(jack) AS number,
            split_part(jack,'-',3) AS floor,
            split_part(jack,'-',4) AS room
            FROM access_points WHERE split_part(jack,'-',2)=""" + 
            dbconn.adapt(str(params['building'].value)).getquoted() + """
            GROUP BY floor,room
            ORDER BY floor,room
    """) 

    arr = {}
    for row in con:
        if row['floor'] in arr:
            arr[row['floor']].append(row['room'])
        else:
            arr[row['floor']] = [row['room']]

    res = []
    for k in arr:
        res.append({'floor':k, 'rooms':arr[k]})

    dbconn.send_array_as_json(res)

jbybid()
