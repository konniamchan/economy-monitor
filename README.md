# Economy Monitor
Economy monitor using Twitter data. Data storage and retrieval project (MIDS W205).

## Organization

### setup
- Brief instructions to set up environment using Amazon Linux.

### ingestion
- Ingest Twitter stream data with Kafka (twitter_ingest.py)
- Write tweets from Kafka to MongoDB and write hourly tweet ID's to PostgreSQL (twitter_write.py)
- Download initial jobless claims and S&P500 data from Quandl (quandl_loading.sh)
- Load Quandl data into PostgreSQL (quandl_loading.sql)
- Bring PostgreSQL's Quandl data up to date to today (quandl_update.py)

### processing
- Count keywords from tweets using regular expression matching; run on an hourly basis (twitter_process.py)
- Process all tweets in MongoDB instead of hourly (twitter_batch.py)

### streaming
- Real-time keyword frequency processing with Spark Streaming (twitter_spark.py)

### visualization
- Tableau dashboards and associated png's

### screenshots
- A few screenshots of Kafka, PostgreSQL, and Spark
