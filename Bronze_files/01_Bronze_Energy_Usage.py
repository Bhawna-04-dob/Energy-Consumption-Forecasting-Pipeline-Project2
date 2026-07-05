# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# Step 1.3 - Set Catalog & Schema
spark.sql("USE CATALOG Bronze_Catalog")
spark.sql("USE SCHEMA Bronze_SCH")

# COMMAND ----------

# Step 1.4 - Read Parquet from ADLS

# Replace <storage-account> with your storage account name.

energy_df = spark.read.parquet(
    "abfss://rev1@adlsstgacnt2026.dfs.core.windows.net/Parquet_files/energy_usage_stream_v2.parquet"
)

# Step 1.5 - Verify Data
display(energy_df)

# COMMAND ----------

# Step 1.6 - Verify Schema
energy_df.printSchema()

# COMMAND ----------

# Step 1.7 - Check Record Count
print(energy_df.count())

# COMMAND ----------

# Step 1.8 - Write Bronze Table
energy_df.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Energy_Usage")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

try:

    energy_df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Energy_Usage")

    spark.sql(f"""
        INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
        VALUES(
            'Bronze_Energy_Usage',
            'Energy Bronze Pipeline',
            current_timestamp(),
            {energy_df.count()},
            'SUCCESS',
            NULL
        )
    """)

    print("Data Loaded Successfully")

except Exception as e:

    spark.sql(f"""
        INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
        VALUES(
            'Bronze_Energy_Usage',
            'Energy Bronze Pipeline',
            current_timestamp(),
            0,
            'FAILED',
            '{str(e)}'
        )
    """)

    raise

# COMMAND ----------

record_count = energy_df.count()

# COMMAND ----------

spark.sql(f"""
INSERT INTO Bronze_Catalog.Bronze_SCH.Audit_Log
VALUES (
    'Bronze_Energy_Usage',
    'Energy Bronze Pipeline',
    current_timestamp(),
    {record_count},
    'SUCCESS',
    NULL
)
""")

# COMMAND ----------

from pyspark.sql.functions import to_timestamp, col

energy_df = energy_df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"), "dd-MM-yyyy HH:mm")
)

# COMMAND ----------

energy_df.printSchema()

# COMMAND ----------

# Read Last Watermark
from pyspark.sql.functions import col

last_watermark = spark.sql("""
SELECT last_processed_timestamp
FROM Bronze_Catalog.Bronze_SCH.Watermark_Table
WHERE table_name='Bronze_Energy_Usage'
""").collect()[0][0]

print(last_watermark)

# COMMAND ----------

# Step 5.2 Filter Only New Records
incremental_df = energy_df.filter(
    col("timestamp") > last_watermark
)

# COMMAND ----------

# Step 5.3 Check Count
incremental_df.count()

# COMMAND ----------

energy_df.select("timestamp").show(10, False)

# COMMAND ----------

# Cell 4 - Verify
display(incremental_df.limit(10))

# COMMAND ----------

incremental_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("Bronze_Catalog.Bronze_SCH.Bronze_Energy_Usage")

# COMMAND ----------

