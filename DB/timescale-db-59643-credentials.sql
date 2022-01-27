/****  GET STARTED WITH YOUR TIMESCALE CLOUD SERVICE  ****/


/*
SERVICE INFORMATION:

Service name:  db-59643
Database name: tsdb
Username:      tsdbadmin
Password:      s076ypajb1f2sx6z
Service URL:   postgres://tsdbadmin:s076ypajb1f2sx6z@sjlvg6tey5.y7ed71zc7s.tsdb.cloud.timescale.com:39863/tsdb?sslmode=require
Port:          39863

~/.pg_service.conf
echo "
[db-59643]
host=sjlvg6tey5.y7ed71zc7s.tsdb.cloud.timescale.com
port=39863
user=tsdbadmin
password=s076ypajb1f2sx6z
dbname=tsdb
" >> ~/.pg_service.conf
psql -d "service=db-59643"
*/

----------------------------------------------------------------------------

/*  
 ╔╗
╔╝║
╚╗║
 ║║         CONNECT TO YOUR SERVICE
╔╝╚╦╗
╚══╩╝
 
 ​
1. Install psql:
    https://blog.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/

2. From your command line, run:
    psql "postgres://tsdbadmin:s076ypajb1f2sx6z@sjlvg6tey5.y7ed71zc7s.tsdb.cloud.timescale.com:39863/tsdb?sslmode=require"
*/

----------------------------------------------------------------------------

/*
╔═══╗
║╔═╗║
╚╝╔╝║	
╔═╝╔╝	    CREATE A HYPERTABLE
║ ╚═╦╗
╚═══╩╝  
*/

CREATE TABLE conditions (	-- create a regular table
    time        TIMESTAMPTZ       NOT NULL,
    location    TEXT              NOT NULL,
    temperature DOUBLE PRECISION  NULL
);

SELECT create_hypertable('conditions', 'time');	-- turn it into a hypertable

----------------------------------------------------------------------------

/*  
╔═══╗
║╔═╗║
╚╝╔╝║	
╔╗╚╗║      INSERT DATA
║╚═╝╠╗
╚═══╩╝	 
*/

INSERT INTO conditions
  VALUES
    (NOW(), 'office', 70.0),
    (NOW(), 'basement', 66.5),
    (NOW(), 'garage', 77.0);
​
----------------------------------------------------------------------------

/*
FOR MORE DOCUMENTATION AND GUIDES, VISIT	>>>--->	HTTPS://DOCS.TIMESCALE.COM/
*/