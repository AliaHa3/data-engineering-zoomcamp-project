# Data Engineering | Zoomcamp Course Project

![image](https://user-images.githubusercontent.com/98602171/235377169-8e02e9a5-1cfd-4812-9607-e2bf842867c4.png)



### Problem statement

The project aims to build an end-to-end data pipeline that extracts earthquake data periodically (hourly) from  [**USGS API**](https://www.usgs.gov/about). The extracted data will be processed and enriched with a new geo column (city) that will be extracted from one of the existing columns that have a long address (place) then create desired tables for our dashboard to generate analytics.

There will be two running pipelines (DAG):
- **Hourly_DAG**: this DAG will run hourly to extract new data starting from the installation time.
- **Historical_DAG**: this DAG will run once to extract the historical earthquake data (2020, 2021, 2022, 2023 till today).

The dashboard will have three parts with control filters on time and city that demonstrate the analytics points below:
* **Historical data analytics:**
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)
* **Spatial data analytics:**
    * World map with earthquakes geolocation
    * Heat world map that shows the earthquakes mags (intense)
* **Last 24 hours analytics:**
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)

To accelerate queries and data processing, the final table "full_data" has been partitioned by date of earthquakes (column 'time') as this column is one of the filter control in the dashboard also one of the dashboard's sections considers taking the latest date partition only (where the date is equal today) and the table is clustered by geodata (column 'city') which is a filter control in the dashboard too.
The original column 'time' type is transformed from string to date type in order to be able to partition by time in spark transformation steps.

![image](https://user-images.githubusercontent.com/98602171/235377176-1eeff0b9-18f7-4e1b-b688-b878fb87b92f.png)


## Data Pipeline 

* **Full pipeline**
   ![image](https://user-images.githubusercontent.com/98602171/235487296-0b2d9eb4-89ec-405a-81c2-3bfca8c315db.png)

* **Hourly_DAG**
   ![image](https://user-images.githubusercontent.com/98602171/235377455-f82b774d-c4fe-425a-b813-aa3c6b18f697.png)

* **Historical_DAG**
   ![image](https://user-images.githubusercontent.com/98602171/235377439-be686e2c-1d4e-478c-a55d-887c6821bb57.png)


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



## Analytics Dashboard

The dashboard will have three parts with control filters on time and city that demonstrate the analytics points below:
* Historical data analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)
    ![image](https://user-images.githubusercontent.com/98602171/235377306-51f21e4b-d37d-48fc-a4a8-a1d51ed91c64.png)

* Spatial data analytics:
    * World map with earthquakes geolocation
    * Heat world map that shows the earthquakes mags (intense)
    ![image](https://user-images.githubusercontent.com/98602171/235377334-bf23efb2-4ce8-4296-86cf-50e4b222f063.png)

* Last 24 hours analytics:
    * Earthquakes trending with times
    * Earthquakes counts per city
    * Maximum intense earthquakes (mag)
    ![image](https://user-images.githubusercontent.com/98602171/235377357-4325c04d-b3a5-44e5-b8c1-ef878eb4278f.png)

You can check the live dashboard [**here**](https://lookerstudio.google.com/reporting/dedce778-8abd-492c-9bce-97b199d5fdfa) (Please note that the live dashboad may be not working as the free tier of google cloud will end soon).

## Setup

1. Setup your google cloud machine project and compute machine [step1](setup/gcp_vm.md)
2. Clone the repo
    ```bash
    git clone https://github.com/AliaHa3/data-engineering-zoomcamp-project.git
    ```
3. Setup terraform [step2](setup/terraform_vm.md)
4. Setup Anaconda + docker  + docker-compose
     ```bash
    cd data-engineering-zoomcamp-project
    bash scripts/vm_setup.sh
    ```
5. Update the enviroment variables in below file with your specific project_id and buckets
    ```bash
    cat data-engineering-zoomcamp-project/scripts/setup_config.sh
    ```
6. Setup pipeline docker image (airflow+spark)
     ```bash
    cd data-engineering-zoomcamp-project
    bash scripts/airflow_startup.sh
    ```
7. in Visual Studio code click on ports and forward port 8080<br>
  ![ForwardPort](https://user-images.githubusercontent.com/7443591/160403735-7c40babc-7d63-4b51-90da-c065e5b254a0.png)

go to localhost:8080<br>
  
and login with (airflow:airflow) for the credentials<br>
![AirflowLogin](https://user-images.githubusercontent.com/7443591/160413081-4f4e606f-09f6-4d4f-9b94-5241f37091a6.png)

8. Enable the historical_DAG and you should see it run. It takes 10-15 minutres to finish
9. Enable the hourly_DAG
10. You can check your data in bigquery tables.