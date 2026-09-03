# Bronze ingestion

## Purpose

## Load raw cloud billing data without applying business transformations.

## Bronze-layer responsibilities

##- Preserve the source fields
##- Add ingestion metadata
##- Enforce a basic schema
##- Record malformed or incomplete rows
##- Write the result as a Delta table

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DateType,
    DoubleType,
)

cloud_cost_schema = StructType([
    StructField("billing_date", DateType(), False),
    StructField("provider", StringType(), True),
    StructField("billing_account_id", StringType(), True),
    StructField("resource_id", StringType(), True),
    StructField("service_name", StringType(), False),
    StructField("usage_type", StringType(), True),
    StructField("region", StringType(), True),
    StructField("team", StringType(), True),
    StructField("project", StringType(), True),
    StructField("environment", StringType(), True),
    StructField("usage_quantity", DoubleType(), True),
    StructField("usage_unit", StringType(), True),
    StructField("cost_amount", DoubleType(), False),
    StructField("currency", StringType(), True),
])

# Planned ingestion metadata:
# - ingestion_timestamp
# - source_file_name
# - ingestion_date
# - record_id

from pyspark.sql import functions as F

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DateType,
    DoubleType,
)

cloud_cost_schema = StructType([
    StructField(
        "billing_date",
        DateType(),
        True,
    ),
    StructField(
        "provider",
        StringType(),
        True,
    ),
    StructField(
        "billing_account_id",
        StringType(),
        True,
    ),
    StructField(
        "resource_id",
        StringType(),
        True,
    ),
    StructField(
        "service_name",
        StringType(),
        True,
    ),
    StructField(
        "usage_type",
        StringType(),
        True,
    ),
    StructField(
        "region",
        StringType(),
        True,
    ),
    StructField(
        "team",
        StringType(),
        True,
    ),
    StructField(
        "project",
        StringType(),
        True,
    ),
    StructField(
        "environment",
        StringType(),
        True,
    ),
    StructField(
        "usage_quantity",
        DoubleType(),
        True,
    ),
    StructField(
        "usage_unit",
        StringType(),
        True,
    ),
    StructField(
        "cost_amount",
        DoubleType(),
        True,
    ),
    StructField(
        "currency",
        StringType(),
        True,
    ),
])

df_raw = spark.table("dbacademy.default.cloud_costs")

display(df_raw.limit(20))

df_raw.printSchema()


from pyspark.sql import functions as F

source_columns = df_raw.columns

record_string = F.concat_ws(
    "||",
    *[
        F.coalesce(
            F.col(column).cast("string"),
            F.lit("<NULL>")
        )
        for column in source_columns
    ]
)

df_bronze = (
    df_raw
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_ingestion_date", F.current_date())
    .withColumn("_record_hash", F.sha2(record_string, 256))
)

display(df_bronze.limit(20))

print("Rows:", df_bronze.count())