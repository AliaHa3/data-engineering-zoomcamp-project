# Data Engineering | Zoomcamp Course Project

![image](https://user-images.githubusercontent.com/98602171/235354699-40962ebf-4d05-43f0-a509-a236f77fd10f.png)

![image](https://user-images.githubusercontent.com/98602171/235377169-8e02e9a5-1cfd-4812-9607-e2bf842867c4.png)



### Problem statement

The project aims to build an end-to-end data pipeline that extracts earthquake data periodically (hourly) from  [**USGS API**](https://www.usgs.gov/about). The extracted data will be processed and enriched with a new geo column (city) that will be extracted from one of the existing columns that have a long address (place) then create desired tables for our dashboard to generate analytics.

There will be two running pipelines (DAG):
- Hourly_DAG: this DAG will run hourly to extract new data starting from the installation time.
- Historical_DAG: this DAG will run once to extract the historical earthquake data (2020, 2021, 2022, 2023 till today).

The dashboard will have three parts with control filters on time and city that demonstrate the analytics points below:
* Historical data analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)
* Spatial data analytics:
    * World map with earthquakes geolocation
    * Heat world map that shows the earthquakes mags (intense)
* Last 24 hours analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)

To accelerate queries and data processing, the final table "full_data" has been partitioned by date of earthquakes (column 'time') as this column is one of the filter control in the dashboard also one of the dashboard's sections considers taking the latest date partition only (where the date is equal today) and the table is clustered by geodata (column 'city') which is a filter control in the dashboard too.
The original column 'time' type is transformed from string to date type in order to be able to partition by time in spark transformation steps.

![image](https://user-images.githubusercontent.com/98602171/235377176-1eeff0b9-18f7-4e1b-b688-b878fb87b92f.png)



## Data Pipeline 

The pipeline could be stream or batch: this is the first thing you'll need to decide 

* If you want to consume data in real-time and put them to data lake - go with stream.
* If you want to run things periodically (e.g. hourly/daily), go with batch

* Hourly_DAG

* Historical_DAG



## Technologies and Tools

- Cloud - [**Google Cloud Platform**](https://cloud.google.com)
- Infrastructure as Code software (IaC) - [**Terraform**](https://www.terraform.io)
-  Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Workflow Orchestration - [**Airflow**](https://airflow.apache.org)
- Batch processing - [**Apache Spark**](https://spark.apache.org/)
- Data Lake - [**Google Cloud Storage**](https://cloud.google.com/storage)
- Data Warehouse - [**BigQuery**](https://cloud.google.com/bigquery)
- Data Visualization - [**Looker Studio (Google Data Studio)**](https://lookerstudio.google.com/overview?)
- Language - [**Python**](https://www.python.org)

## Dashboard

The dashboard will have three parts with control filters on time and city that demonstrate the analytics points below:
* Historical data analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)
* Spatial data analytics:
    * World map with earthquakes geolocation
    * Heat world map that shows the earthquakes mags (intense)
* Last 24 hours analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)

Example of a dashboard: ![image](https://user-images.githubusercontent.com/4315804/159771458-b924d0c1-91d5-4a8a-8c34-f36c25c31a3c.png)


## Setup

## Peer review criteria

* Problem description
    * 0 points: Problem is not described
    * 1 point: Problem is described but shortly or not clearly 
    * 2 points: Problem is well described and it's clear what the problem the project solves
* Cloud
    * 0 points: Cloud is not used, things run only locally
    * 2 points: The project is developed in the cloud
    * 4 points: The project is developed in the cloud and IaC tools are used
* Data ingestion (choose either batch or stream)
    * Batch / Workflow orchestration
        * 0 points: No workflow orchestration
        * 2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
        * 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
    * Stream
        * 0 points: No streaming system (like Kafka, Pulsar, etc)
        * 2 points: A simple pipeline with one consumer and one producer
        * 4 points: Using consumer/producers and streaming technologies (like Kafka streaming, Spark streaming, Flink, etc)
* Data warehouse
    * 0 points: No DWH is used
    * 2 points: Tables are created in DWH, but not optimized
    * 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
* Transformations (dbt, spark, etc)
    * 0 points: No tranformations
    * 2 points: Simple SQL transformation (no dbt or similar tools)
    * 4 points: Tranformations are defined with dbt, Spark or similar technologies
* Dashboard
    * 0 points: No dashboard
    * 2 points: A dashboard with 1 tile
    * 4 points: A dashboard with 2 tiles
* Reproducibility
    * 0 points: No instructions how to run code at all
    * 2 points: Some instructions are there, but they are not complete
    * 4 points: Instructions are clear, it's easy to run the code, and the code works
