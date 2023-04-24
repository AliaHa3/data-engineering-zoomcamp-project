import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import argparse
import os

SERVICE_ACCOUNT_JSON_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


# parser = argparse.ArgumentParser()

# parser.add_argument('--input_file', required=True,default="")
# parser.add_argument('--output_file', required=True,default="")
# parser.add_argument('--output_table', required=True,default="")

# args = parser.parse_args()

# input_file = args.input_file
# output_file = args.output_file
# output_table = args.output_table

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
print(spark.version)

spark._jsc.hadoopConfiguration().set("google.cloud.auth.service.account.json.keyfile","SERVICE_ACCOUNT_JSON_PATH")

path = "gs://earthquakes_data_lake_dezoomcamp-375819/earthquakes/data_20230424T090501_20230424T100501_20230424100501.csv.gz"
df=spark.read.csv(path, header=True)
df.show()