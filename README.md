\# Real Time Clickstream Analytics Pipeline



A real time data engineering pipeline built on AWS that processes 

user clickstream events and enables SQL analytics.



\## Architecture



producer.py → SQS → Lambda → S3 → Glue → Athena



\## AWS Services Used



\- Amazon SQS — event queue buffer

\- AWS Lambda — serverless event processing

\- Amazon S3 — data lake storage (JSON and Parquet)

\- AWS Glue — schema cataloging and ETL

\- Amazon Athena — SQL analytics



\## Pipeline Flow



1\. Producer generates fake clickstream events (page views, clicks, purchases)

2\. Events are sent to SQS queue

3\. Lambda processes events in batches of 10

4\. Lambda enriches events (adds processed\_at, is\_conversion, page\_category)

5\. Enriched events saved to S3 partitioned by year/month/day

6\. Glue Crawler catalogs the schema

7\. Glue ETL converts JSON to Parquet format

8\. Athena queries data using SQL



\## Key Concepts Learned



\- Real time event streaming

\- Serverless data processing

\- Data lake partitioning (Hive format)

\- ETL transformation

\- Columnar storage (Parquet vs JSON)

\- SQL analytics on S3



\## Sample Queries

```sql

\-- Conversion funnel

SELECT event\_type, COUNT(\*) AS total

FROM events

GROUP BY event\_type

ORDER BY total DESC;



\-- Device breakdown

SELECT device, COUNT(\*) AS total

FROM events

GROUP BY device;

```



\## Setup Instructions



1\. Create AWS SQS queue named clickstream-queue

2\. Create S3 bucket for processed data

3\. Deploy Lambda function with SQS trigger

4\. Run Glue Crawler to catalog schema

5\. Run Glue ETL job to convert to Parquet

6\. Query with Athena

