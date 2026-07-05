# Databricks notebook source
# Step 1 - Import Libraries
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# Step 2 - Use Catalog & Schema
spark.sql("USE CATALOG Bronze_Catalog")
spark.sql("USE SCHEMA Bronze_SCH")

# COMMAND ----------

# Step 3 - Read Parquet File
device_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/device_metrics_stream_v2.parquet"
)

# COMMAND ----------

# Step 4 - Check Schema
device_df.printSchema()

# COMMAND ----------

# Step 5 - Check Sample Data
display(device_df.limit(10))

# COMMAND ----------

# Step 2 - Check for duplicates


device_df.select("household_id").distinct().count()

# COMMAND ----------

device_df.columns


# COMMAND ----------

device_df.count()

# COMMAND ----------

# Bronze Table
device_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema","true") \
    .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Device_Metrics")

# COMMAND ----------

# Audit Log

record_count = device_df.count()

spark.sql(f"""
INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
VALUES
(
'Bronze_Device_Metrics',
'Device Bronze Pipeline',
current_timestamp(),
{record_count},
'SUCCESS',
NULL
)
""")

# COMMAND ----------

# Create a dummy ingestion timestamp during Bronze loading:
from pyspark.sql.functions import current_timestamp

device_df = device_df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# COMMAND ----------

device_df.printSchema()

# COMMAND ----------

