#!/usr/bin/env python

import dbconn
import jenks

def mactrac():
    query = """ SELECT 
    -- Combine metadata with building info
    buildings.cartodb_id,
    apdata.jacksqft,
    apdata.sqftjack,
    apdata.buildingarea,
    apdata.jackcount,
    buildings.name,
    ST_AsGeoJSON(buildings.the_geom) AS the_geom,
    ST_AsGeoJSON(st_centroid(buildings.the_geom)) AS centroid, 
    buildings.building_n
    FROM 
    buildings 
    LEFT JOIN 
    (
        -- Get a ratio of room area to jack count
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
                    ELSE  sum(b.shape_area)
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

    ) apdata ON (apdata.building = buildings.building_n)
    ORDER BY apdata.jacksqft
    """

    # Extract just the jacks/area and jenks it
    rows = dbconn.run_query(query).fetchall()
    jacksqft = []
    for row in rows:
        if(row['jacksqft'] != None):
            jacksqft.append(row['jacksqft'])
    breaks = jenks.getJenksBreaks(jacksqft, 5)

    # Add that info into the resulting data
    for row in rows:
        if(row['jacksqft'] == None):
            row['jenks'] = None
        else:
            row['jenks'] = jenks.classify(row['jacksqft'], breaks)

    geojson = dbconn.array_to_geojson(rows)
    dbconn.send_array_as_json(geojson)

mactrac()
