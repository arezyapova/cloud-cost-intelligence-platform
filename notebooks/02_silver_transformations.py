from pyspark.sql import functions as F

df_bronze = spark.table(
    "cloud_cost_intelligence.bronze_cloud_costs"
)
display(df_bronze.limit(20))
print(df_bronze.count())
df_bronze.groupBy("environment").count().show()
df_bronze.select(
    F.sum(
        F.when(
            F.col("team").isNull() |
            (F.trim(F.col("team")) == ""),
            1
        ).otherwise(0)
    ).alias("missing_team"),
    
    F.sum(
        F.when(
            F.col("project").isNull() |
            (F.trim(F.col("project")) == ""),
            1
        ).otherwise(0)
    ).alias("missing_project")
).show()

(
    df_bronze
    .groupBy("_record_hash")
    .count()
    .filter(F.col("count") > 1)
    .show()
)

df_silver = (
    df_bronze

    .withColumn(
        "team",
        F.when(
            F.col("team").isNull() |
            (F.trim(F.col("team")) == ""),
            F.lit("Unallocated")
        ).otherwise(
            F.trim(F.col("team"))
        )
    )

    .withColumn(
        "project",
        F.when(
            F.col("project").isNull() |
            (F.trim(F.col("project")) == ""),
            F.lit("Unallocated")
        ).otherwise(
            F.trim(F.col("project"))
        )
    )
)

df_silver = (
    df_silver
    .withColumn(
        "environment",
        F.when(
            F.lower(F.trim(F.col("environment"))).isin(
                "prod",
                "production"
            ),
            "Production"
        )
        .when(
            F.lower(F.trim(F.col("environment"))).isin(
                "dev",
                "development"
            ),
            "Development"
        )
        .when(
            F.lower(F.trim(F.col("environment"))).isin(
                "test"
            ),
            "Test"
        )
        .otherwise(
            F.initcap(
                F.trim(F.col("environment"))
            )
        )
    )
)

df_silver = (
    df_silver
    .dropDuplicates(
        ["_record_hash"]
    )
)

print(
    "Bronze rows:",
    df_bronze.count()
)

print(
    "Silver rows:",
    df_silver.count()
)

df_silver = (
    df_silver
    .withColumn(
        "billing_month",
        F.date_trunc(
            "month",
            F.col("billing_date")
        )
    )
    .withColumn(
        "allocation_status",
        F.when(
            (F.col("team") == "Unallocated") |
            (F.col("project") == "Unallocated"),
            "Unallocated"
        ).otherwise(
            "Allocated"
        )
    )
)

display(
    df_silver.select(
        "billing_date",
        "billing_month",
        "provider",
        "team",
        "project",
        "environment",
        "allocation_status",
        "cost_amount"
    ).limit(20)
)

df_silver.groupBy(
    "environment"
).count().show()

df_silver.groupBy(
    "allocation_status"
).count().show()

duplicate_count = (
    df_silver
    .groupBy("_record_hash")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print(
    "Duplicate hashes:",
    duplicate_count
)

df_silver.select(
    F.sum(
        F.when(
            F.col("billing_date").isNull(),
            1
        ).otherwise(0)
    ).alias("missing_date"),

    F.sum(
        F.when(
            F.col("service_name").isNull(),
            1
        ).otherwise(0)
    ).alias("missing_service"),

    F.sum(
        F.when(
            F.col("cost_amount").isNull(),
            1
        ).otherwise(0)
    ).alias("missing_cost")
).show()

(
    df_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "cloud_cost_intelligence.silver_cloud_costs"
    )
)

silver_check = spark.table(
    "cloud_cost_intelligence.silver_cloud_costs"
)

print(silver_check.count())

display(
    silver_check.limit(20)
)
