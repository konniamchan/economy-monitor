# Quandl to Postgres
import Quandl
import pandas as pd
import psycopg2 as pg
import datetime as dt

# PostgreSQL connection
conn    = pg.connect(user='w205',database='w205project',password='pw')
cur     = conn.cursor()
current_date = dt.datetime.now().strftime("%Y-%m-%d")


# Update tables
table_info = {"claims": {"quandl": 'FRED/ICNSA'}, "gspc":{"quandl": 'YAHOO/INDEX_GSPC.6'}}

for table, values in table_info.items():
	# Get last update dates
	cur.execute("SELECT max(date) FROM " + table)
	last_update = cur.fetchone()[0]
	conn.commit()

	# Update new data
	new_data = Quandl.get(values["quandl"], trim_start = (last_update + dt.timedelta(days=1)).strftime("%Y-%m-%d"), trim_end=current_date)
	for row in new_data.itertuples():
		cur.execute("INSERT INTO " + table + " VALUES (%s, %s)", (row[0], row[1]))
		conn.commit()

cur.close()
conn.close()