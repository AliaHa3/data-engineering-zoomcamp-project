import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('--input_file', required=True,default="")
parser.add_argument('--output_file', required=True,default="")
parser.add_argument('--output_table', required=True,default="")

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
output_table = args.output_table

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
print(spark.version)
