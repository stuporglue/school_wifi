#!/usr/bin/env python

import psycopg2
import psycopg2.extras
from psycopg2.extensions import adapt
import ConfigParser

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


