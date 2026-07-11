# Databricks notebook source
# Step 1 - Import Libraries
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# Step 2 - Use Catalog & Schema
spark.sql("USE CATALOG Bronze_Catalog")
spark.sql("USE SCHEMA Bronze_SCH")

# COMMAND ----------

# Step 3 - Read Parquet
tariff_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/tariff_metrics_stream_v2.parquet"
)

# COMMAND ----------

# Step 4 - Check Schema
tariff_df.printSchema()

# COMMAND ----------

# Step 5 - Check Columns
tariff_df.columns

# COMMAND ----------

# Step 6 - Add Ingestion Timestamp
from pyspark.sql.functions import current_timestamp

tariff_df = tariff_df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# COMMAND ----------

# Step 7 - Verify
tariff_df.printSchema()

# COMMAND ----------

# Step 8 - Create Bronze Table
tariff_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema","true") \
    .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Tariff_Metrics")

# COMMAND ----------

# Step 10 - Insert Audit Log
record_count = tariff_df.count()

spark.sql(f"""
INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
VALUES
(
'Bronze_Tariff_Metrics',
'Tariff Bronze Pipeline',
current_timestamp(),
{record_count},
'SUCCESS',
NULL
)
""")

# COMMAND ----------

