-- Initial creation and loading of economic data databases

-- FRED initial claims data
CREATE TABLE claims (
	date DATE NOT NULL PRIMARY KEY,
	initial_claims REAL NOT NULL
);
\copy claims FROM '/home/ec2-user/quandl_data/claims.csv' CSV HEADER;


-- S&P500 index data
CREATE TABLE GSPC (
	date DATE NOT NULL PRIMARY KEY,
	index_value DOUBLE PRECISION NOT NULL
);
\copy GSPC FROM '/home/ec2-user/quandl_data/GSPC.csv' CSV HEADER;
