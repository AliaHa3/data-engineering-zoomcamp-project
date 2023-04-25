import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import types
import argparse
import os

from geopy.geocoders import Nominatim
from geopy.point import Point
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="geoapiEnrichment")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

full_columns = [
    "time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap", "dmin", "rms",
    "net", "id", "updated", "place", "type", "horizontalError", "depthError", "magError",
    "magNst", "status", "locationSource", "magSource", "city", "state", "country", "country_code", "zipcode"
]
schema = types.StructType(
    [
        types.StructField("time", types.TimestampType(), True),
        types.StructField("latitude", types.FloatType(), True),
        types.StructField("longitude", types.FloatType(), True),
        types.StructField("depth", types.FloatType(), True),
        types.StructField("mag", types.FloatType(), True),
        types.StructField("magType", types.StringType(), True),
        types.StructField("nst", types.FloatType(), True),
        types.StructField("gap", types.FloatType(), True),
        types.StructField("dmin", types.FloatType(), True),
        types.StructField("rms", types.FloatType(), True),
        types.StructField("net", types.StringType(), True),
        types.StructField("id", types.StringType(), True),
        types.StructField("updated", types.TimestampType(), True),
        types.StructField("place", types.StringType(), True),
        types.StructField("type", types.StringType(), True),
        types.StructField("horizontalError", types.FloatType(), True),
        types.StructField("depthError", types.FloatType(), True),
        types.StructField("magError", types.FloatType(), True),
        types.StructField("magNst", types.FloatType(), True),
         types.StructField("status", types.StringType(), True),
        types.StructField("locationSource", types.StringType(), True),
        types.StructField("magSource", types.StringType(), True)
    ]
)

enrich_schema = types.StructType(
    [
        types.StructField("time", types.TimestampType(), True),
        types.StructField("latitude", types.FloatType(), True),
        types.StructField("longitude", types.FloatType(), True),
        types.StructField("depth", types.FloatType(), True),
        types.StructField("mag", types.FloatType(), True),
        types.StructField("magType", types.StringType(), True),
        types.StructField("nst", types.FloatType(), True),
        types.StructField("gap", types.FloatType(), True),
        types.StructField("dmin", types.FloatType(), True),
        types.StructField("rms", types.FloatType(), True),
        types.StructField("net", types.StringType(), True),
        types.StructField("id", types.StringType(), True),
        types.StructField("updated", types.TimestampType(), True),
        types.StructField("place", types.StringType(), True),
        types.StructField("type", types.StringType(), True),
        types.StructField("horizontalError", types.FloatType(), True),
        types.StructField("depthError", types.FloatType(), True),
        types.StructField("magError", types.FloatType(), True),
        types.StructField("magNst", types.FloatType(), True),
         types.StructField("status", types.StringType(), True),
        types.StructField("locationSource", types.StringType(), True),
        types.StructField("magSource", types.StringType(), True),
        types.StructField("city", types.StringType(), True),
        types.StructField("state", types.StringType(), True),
        types.StructField("country", types.StringType(), True),
        types.StructField("country_code", types.StringType(), True),
        types.StructField("zipcode", types.StringType(), True)
    ]
)

SERVICE_ACCOUNT_JSON_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
SPARK_GCS_JAR = "/opt/airflow/lib/gcs-connector-hadoop3-2.2.5.jar"
SPARK_BQ_JAR = "/opt/airflow/lib/spark-bigquery-latest_2.12.jar"


def country_enrichment(row):
    geolocator = Nominatim(user_agent="geoapiEnrichment")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    print("inside")
    # location = geolocator.reverse(Point(row['latitude'],row['longitude']))
    location = reverse(Point(row['latitude'], row['longitude']))
    address = {}
    if location is not None:
        address = location.raw['address']

    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    country_code = address.get('country_code', '')
    zipcode = address.get('postcode', '')

    return (
        row["time"], row["latitude"], row["longitude"], row["depth"], row["mag"], row["magType"], row["nst"], row["gap"], row["dmin"], row["rms"], row["net"], row["id"], row["updated"], row["place"], row["type"], row["horizontalError"], row["depthError"], row["magError"], row["magNst"], row["status"], row["locationSource"], row["magSource"], city, state, country, country_code, zipcode)


# parser = argparse.ArgumentParser()

# parser.add_argument('--input_file', required=True,default="")
# parser.add_argument('--output_file', required=True,default="")
# parser.add_argument('--output_table', required=True,default="")

# args = parser.parse_args()

# input_file = args.input_file
# output_file = args.output_file
# output_table = args.output_table

tmp_bucket = "dtc_data_lake_dezoomcamp-375819"

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", f"{SPARK_GCS_JAR},{SPARK_BQ_JAR}") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", SERVICE_ACCOUNT_JSON_PATH) \
    .set('temporaryGcsBucket', tmp_bucket)

sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.AbstractFileSystem.gs.impl",
                "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set(
    "fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile",
                SERVICE_ACCOUNT_JSON_PATH)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

path = "gs://earthquakes_data_lake_dezoomcamp-375819/earthquakes/data_20230424T090501_20230424T100501_20230424100501.csv.gz"
df = (
    spark.read.option("header", "true").schema(schema).csv(path)
)
df.show()
df.printSchema()

# df = spark.read.csv(path, header=True)
# df.show()

enrich_rdd = df.rdd.map(lambda row: country_enrichment(row))
# new_df.collect()
# new_df = new_df.toDF(full_columns)


new_df = spark.createDataFrame(enrich_rdd, schema=enrich_schema)
new_df.printSchema()
new_df.show()

new_df.write.format('bigquery') \
    .option('table', 'earthquake_prod.tmptable2') \
    .mode('overwrite') \
    .save()
