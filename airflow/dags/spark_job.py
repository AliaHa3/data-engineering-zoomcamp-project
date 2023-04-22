import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
print(spark.version)
