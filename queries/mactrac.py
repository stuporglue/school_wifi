#!/usr/bin/env python

import dbconn

q = """ SELECT 
-- Combine metadata with building info
buildings.cartodb_id,
apdata.apratio,
apdata.roomarea,
apdata.jackcount,
buildings.name,
ST_AsGeoJSON(buildings.the_geom) AS the_geom,
buildings.building_n
FROM 
buildings 
LEFT JOIN 
(
    -- Get a ratio of room area to jack count
    SELECT 
    binfo.building,
 binfo.roomarea,
  jinfo.jackcount,
    (jinfo.jackcount / binfo.roomarea) AS apratio
    FROM 
    (
        -- Get the area of all the rooms for each building
        SELECT
        building,
        SUM(shape_area) AS roomarea
        FROM 
        rooms
        GROUP BY building
    ) binfo,
    (
        -- Get a jack count of each building
        SELECT
        split_part(jack,'-',2) AS building,
        count(jack) AS jackcount
        FROM access_points
        WHERE 
        split_part(jack,'-',2) ~ '^[0-9]+$'
        GROUP BY split_part(jack,'-',2)
    ) jinfo
    WHERE
    binfo.building = jinfo.building

) apdata ON (apdata.building = buildings.building_n)
"""

dbconn.send_geojson(q)
