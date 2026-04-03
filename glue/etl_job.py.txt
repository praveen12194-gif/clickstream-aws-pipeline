import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource = glueContext.create_dynamic_frame.from_catalog(
    database="clickstream_db",
    table_name="events"
)

print(f"Total records read: {datasource.count()}")

df = datasource.toDF()

df.write \
  .mode("overwrite") \
  .partitionBy("year", "month", "day") \
  .parquet("s3a://clickstream-processed-pk/parquet/")

print("Parquet conversion complete!")
job.commit()