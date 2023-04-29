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

SERVICE_ACCOUNT_JSON_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
BQ_DATASET_PROD = os.environ.get('BIGQUERY_DATASET', 'earthquake_prod')
# production_table_name = 'full_data'

SPARK_GCS_JAR = "/opt/airflow/lib/gcs-connector-hadoop3-2.2.5.jar"
SPARK_BQ_JAR = "/opt/airflow/lib/spark-bigquery-latest_2.12.jar"
TMP_BUCKET = "dtc_data_lake_dezoomcamp-375819"
path = "gs://earthquakes_data_lake_dezoomcamp-375819/earthquakes/data_20230424T090501_20230424T100501_20230424100501.csv.gz"


# geolocator = Nominatim(user_agent="geoapiEnrichment")
# reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

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
        types.StructField("city", types.StringType(), True)
    ]
)


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


def country_enrichment_string_func(row):
    print("inside")
    city = None
    if row is not None and row["place"] is not None:
        city = row["place"]
        if ',' in row["place"]:
            city = row["place"].split(',')[-1].strip()
        
    return (
        row["time"], row["latitude"], row["longitude"], row["depth"], row["mag"], row["magType"], row["nst"], row["gap"], row["dmin"], row["rms"], row["net"], row["id"], row["updated"], row["place"], row["type"], row["horizontalError"], row["depthError"], row["magError"], row["magNst"], row["status"], row["locationSource"], row["magSource"], city)


parser = argparse.ArgumentParser()

parser.add_argument('--input_file', required=True)
# parser.add_argument('--country_enrichment_string', default='False')
# parser.add_argument('--output_file', required=True)
# parser.add_argument('--output_table', required=True)

args = parser.parse_args()

input_file = args.input_file
# country_enrichment_string = True if args.country_enrichment_string == 'True' else False
# output_file = args.output_file
# output_table = args.output_table


conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", f"{SPARK_GCS_JAR},{SPARK_BQ_JAR}") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", SERVICE_ACCOUNT_JSON_PATH) \
    .set('temporaryGcsBucket', TMP_BUCKET)

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


df = (
    spark.read.option("header", "true").schema(schema).csv(input_file)
)
df.show()
df.printSchema()

enrich_rdd = df.rdd.map(lambda row: country_enrichment_string_func(row))

enrich_df = spark.createDataFrame(enrich_rdd, schema=enrich_schema)
enrich_df.printSchema()
enrich_df.show()


enrich_df.write.format('bigquery') \
    .option('table', f"{BQ_DATASET_PROD}.full_data2") \
    .option("partitionField", "time") \
    .option("partitionType", "DAY") \
    .option("clusteredFields", "city") \
    .mode('append') \
    .save()

enrich_df.createOrReplaceTempView("enrich_full_data")


earthquake_dwh_df = spark.sql(
"""
select 
date_trunc(time, year) as _year, 
date_trunc(time, month) as _month, 
date_trunc(time, day) as _day,
city,
count(*) earthquakes_total_count, 
max(depth) max_depth,
max(mag) max_mag,
avg(depth) avg_depth,
avg(mag) avg_mag,
from enrich_full_data
group by 1,2,3,4;
"""
)

earthquake_dwh_df.write.format('bigquery') \
    .option('table', f"{BQ_DATASET_PROD}.earthquake_dwh") \
    .option("clusteredFields", "city") \
    .mode('overwrite') \
    .save()