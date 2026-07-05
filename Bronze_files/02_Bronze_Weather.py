# Databricks notebook source
# Step 1 - Read the Weather Parquet File

# Replace the file path if your file name is slightly different.

from pyspark.sql.functions import *
from pyspark.sql.types import *

spark.sql("USE CATALOG Bronze_Catalog")
spark.sql("USE SCHEMA Bronze_SCH")

weather_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/weather_stream_v2.parquet")

# COMMAND ----------

# Step 2 - Verify the Data
display(weather_df)

# COMMAND ----------

# Step 3 - Check Schema
weather_df.printSchema()

# COMMAND ----------

# Step 4 - Convert Timestamp
from pyspark.sql.functions import col, to_timestamp

weather_df = weather_df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"), "dd-MM-yyyy")
)

# COMMAND ----------

# Step 6 - Create Bronze Table
weather_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema","true") \
    .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Weather")

# COMMAND ----------

weather_df.select("timestamp").show(10, False)

# COMMAND ----------

from pyspark.sql.functions import *

weather_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/weather_stream_v2.parquet"
)

# COMMAND ----------

# Step 11 - Insert Audit Log
record_count = weather_df.count()

spark.sql(f"""
INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
VALUES (
'Bronze_Weather',
'Weather Bronze Pipeline',
current_timestamp(),
{record_count},
'SUCCESS',
NULL
)
""")

# COMMAND ----------

