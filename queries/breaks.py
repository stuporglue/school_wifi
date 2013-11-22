#!/usr/bin/env python

import dbconn
import jenks

q = """ 
    SELECT 
    binfo.building,
    binfo.buildingarea,
    jinfo.jackcount,
    (jinfo.jackcount / binfo.buildingarea) AS jacksqft,
    (binfo.buildingarea / jinfo.jackcount ) AS sqftjack
    FROM 
    (
        -- Get the area of all the floors with 
        SELECT 
            b.building_n AS building,
            CASE count(fc.floors)
                WHEN 0 THEN 0
            ELSE  sum(ST_Area(ST_Transform(the_geom,3860)))
            END AS buildingarea 
        FROM
            buildings b
        LEFT JOIN (
            SELECT DISTINCT
                split_part(jack,'-',2) AS building,
                split_part(jack,'-',3) AS floors
            FROM access_points
            WHERE
                split_part(jack,'-',2) ~ '^[0-9]+$'
        ) fc ON (fc.building = b.building_n)
        GROUP BY b.building_n
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
"""

# Extract just the jacks/area and jenks it
rows = dbconn.run_query(q).fetchall();
jacksqft = []
buildings = []
for row in rows:
    if(row['jacksqft'] != None):
        jacksqft.append(row['jacksqft'])
breaks = jenks.getJenksBreaks(jacksqft,5)

dbconn.send_array_as_json(breaks)
