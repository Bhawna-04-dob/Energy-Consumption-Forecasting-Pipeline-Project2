# Databricks notebook source
# Step 1 - Read Parquet
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark.sql("USE CATALOG Bronze_Catalog")
spark.sql("USE SCHEMA Bronze_SCH")

grid_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/grid_load_stream_v2.parquet"
)

# COMMAND ----------

# Step 2 - Check Schema
grid_df.printSchema()


# COMMAND ----------

# Step 3 - Check Columns
grid_df.columns

# COMMAND ----------

# Step 1 - Add Technical Metadata Column
from pyspark.sql.functions import current_timestamp

grid_df = grid_df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# COMMAND ----------

# Step 2 - Verify
grid_df.printSchema()

# COMMAND ----------

# Step 3 - Create Bronze Table
grid_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Grid_Load")

# COMMAND ----------

# Step 5 - Audit Log
record_count = grid_df.count()

spark.sql(f"""
INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
VALUES (
'Bronze_Grid_Load',
'Grid Bronze Pipeline',
current_timestamp(),
{record_count},
'SUCCESS',
NULL
)
""")

# COMMAND ----------

