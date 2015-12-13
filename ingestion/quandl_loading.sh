#! /bin/bash

# Download FRED initial claims data
wget -O claims.csv "https://www.quandl.com/api/v3/datasets/FRED/ICNSA.csv"

# Download S&P500 data
wget -O GSPC.csv "https://www.quandl.com/api/v3/datasets/YAHOO/INDEX_GSPC.csv?column_index=6"