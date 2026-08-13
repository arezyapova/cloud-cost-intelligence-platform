from pyspark.sql import functions as F

bronze = spark.table(
    "cloud_cost_intelligence.bronze_cloud_costs"
)

silver = spark.table(
    "cloud_cost_intelligence.silver_cloud_costs"
)

gold = spark.table(
    "cloud_cost_intelligence.gold_monthly_cloud_costs"
)
print("Bronze rows:", bronze.count())
print("Silver rows:", silver.count())
print("Gold rows:", gold.count())
required_columns = [ "billing_date", "provider", "service_name", "cost_amount", "currency" ] 

for column in required_columns: 
    missing_count = ( silver .filter(F.col(column).isNull()) .count() ) 
print(column, missing_count)
silver.filter( F.col("team").isNull() | (F.trim(F.col("team")) == "") ).count()
silver.filter( F.col("team").isNull() | (F.trim(F.col("project")) == "") ).count()
silver.select( "environment" ).distinct().show()
duplicate_count = ( silver .groupBy("_record_hash") .count() .filter(F.col("count") > 1) .count() ) 

print("Duplicate hashes:", duplicate_count)
silver_total = ( silver .agg(F.sum("cost_amount").alias("total")) .first()["total"] ) 
gold_total = ( gold .agg(F.sum("total_cost").alias("total")) .first()["total"] ) 
difference = silver_total - gold_total 
print("Silver total:", silver_total) 
print("Gold total:", gold_total) 
print("Difference:", difference)
assert abs(difference) < 0.01
assert silver.count() <= bronze.count() 
assert ( silver .filter(F.col("cost_amount").isNull()) .count() == 0 ) 
assert duplicate_count == 0 
assert abs(silver_total - gold_total) < 0.01 

print("All pipeline quality checks passed.")