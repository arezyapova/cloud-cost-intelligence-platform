"""
Gold analytical model for cloud cost intelligence.

Transforms cleaned Silver cloud-cost records into
a monthly analytics-ready dataset for FinOps reporting.
"""

from pyspark.sql import functions as F

df_silver = spark.table(
    "cloud_cost_intelligence.silver_cloud_costs"
)

print("Silver rows:", df_silver.count())
display(df_silver.limit(10))

# Gold Cloud Cost Model

## Grain

## One row represents monthly cloud cost for a unique combination of:

## - billing month
## - provider
## - team
## - project
## - service
## - environment

## Purpose

##  Provide an analytics-ready cost table for FinOps reporting and Power BI.

df_gold = (
    df_silver
    .groupBy(
        "billing_month",
        "provider",
        "team",
        "project",
        "service_name",
        "environment",
        "allocation_status"
    )
    .agg(
        F.sum("cost_amount").alias("total_cost"),
        F.sum("usage_quantity").alias("total_usage"),
        F.count("*").alias("usage_records"),
        F.countDistinct("resource_id").alias("resource_count")
    )
)

display(df_gold.limit(20))

print("Gold rows:", df_gold.count())

df_gold = (
    df_gold
    .withColumn(
        "avg_cost_per_resource",
        F.when(
            F.col("resource_count") > 0,
            F.col("total_cost") / F.col("resource_count")
        )
    )
)

df_gold = (
    df_gold
    .withColumn(
        "is_unallocated",
        F.col("allocation_status") == "Unallocated"
    )
)

df_gold = (
    df_gold
    .withColumn(
        "billing_year",
        F.year("billing_month")
    )
    .withColumn(
        "billing_month_number",
        F.month("billing_month")
    )
)

silver_total = (
    df_silver
    .agg(
        F.sum("cost_amount").alias("total")
    )
    .first()["total"]
)

gold_total = (
    df_gold
    .agg(
        F.sum("total_cost").alias("total")
    )
    .first()["total"]
)

print("Silver total:", silver_total)
print("Gold total:", gold_total)
print("Difference:", silver_total - gold_total)

assert abs(silver_total - gold_total) < 0.01

monthly_cost = (
    df_gold
    .groupBy("billing_month")
    .agg(
        F.sum("total_cost").alias("total_cost")
    )
    .orderBy("billing_month")
)

display(monthly_cost)

team_cost = (
    df_gold
    .groupBy("team")
    .agg(
        F.sum("total_cost").alias("total_cost")
    )
    .orderBy(
        F.desc("total_cost")
    )
)

display(team_cost)

service_cost = (
    df_gold
    .groupBy("service_name")
    .agg(
        F.sum("total_cost").alias("total_cost")
    )
    .orderBy(
        F.desc("total_cost")
    )
)

display(service_cost)

allocation_cost = (
    df_gold
    .groupBy("allocation_status")
    .agg(
        F.sum("total_cost").alias("total_cost")
    )
)

display(allocation_cost)

(
    df_gold
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "cloud_cost_intelligence.gold_monthly_cloud_costs"
    )
)

gold_check = spark.table(
    "cloud_cost_intelligence.gold_monthly_cloud_costs"
)

print("Saved Gold rows:", gold_check.count())

display(gold_check.limit(20))

