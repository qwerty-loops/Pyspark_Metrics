from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, count, sum, avg
import redis

# Starting or retrieving a spark session
spark = SparkSession.builder.appName("NYCTripProcessor").getOrCreate()

# Load the dataset
df = spark.read.parquet("Trip_Data.parquet")

#Adding the hour column, getting hour from pickup_datetime
df = df.withColumn("pickup_hour", hour(df["tpep_pickup_datetime"]))

# Processing Metrics
# Trip Count by Hour, Total Revenue by Hour, Average Fare by Hour

agg_df = df.groupby("pickup_hour").agg(
    count("*").alias("trip_count"),
    sum(df["fare_amount"] + df["tip_amount"]).alias("total_revenue"),
    avg("trip_distance").alias("avg_distance")
)


# Connecting to Redis
r = redis.StrictRedis(host = "redis", port = 6379, db = 0)

for row in agg_df.collect():
    hour_str = f"{int(row['pickup_hour']) :02}:00" #:02 alwys formats the hour to two digits
    print("Writing to Redis:", hour_str, row['trip_count'], row['total_revenue'], row['avg_distance'])
    r.set(f"trips:total:{hour_str}", row["trip_count"])
    r.set(f"revenue:total:{hour_str}", row["total_revenue"])
    r.set(f"distance:avg:{hour_str}", row["avg_distance"])

