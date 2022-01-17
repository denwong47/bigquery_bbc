# bigquery_bbc
 Demonstration Docker image for `extract_http`and `load_datawarehouse` modules:

 `extract_http` https://github.com/denwong47/extract_http \
 `load_warehouse` https://github.com/denwong47/load_datawarehouse

 When run, this container will extract all headlines on bbc.co.uk (Usable only in UK) as well as their thumbnail images as base64, then load the data into a BigQuery table.

 It is intended to be called by a scheduler such as crontab, systemctl timers or Google Cloud Scheduler etc so that headlines can be analysed across time.

 Proof of concept, not designed for production use.


# Installation and Configuration
The container needs to be configured and built before use. Namely:
- Install Docker
- Obtain API key from Google Cloud Platform
- Configure /Dockerfile
- Configure /main/app/config.py
- Build the container

## Install Docker
Docker can be installed on Windows, macOS or Linux; and containers are not platform dependent.
Please refer to https://docs.docker.com/get-docker/ for ways to obtain Docker.

Docker Compose is not required for this container.

## Obtain API key from Google Cloud Platform
Since this container connects to BigQuery service, an API Key from your Google Cloud Platform is required.
Please refer to https://cloud.google.com/api-keys/docs/get-started-api-keys for details.

To connect to the service, create tables and stream data, the following Roles need to be assigned to the API Key:
- BigQuery Connection User
- BigQuery Data Editor
- BigQuery Job User

You should be able to obtain the API Key in form of a JSON file. This can be stored anywhere in the container; by default the folder /credentials is designed for this purpose.

## Configure /Dockerfile
Line 26 of Dockerfile needs to be adjusted to match your API Key location:
```ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/api-key.json```
The default is located at `/credentials/api-key.json`. (Note that the `/credentials` folder is located at `/app/credentials` inside the image.)

## Configure /main/app/config.py
The following variables need to be set to match your BigQuery setup:
`PROJECT_NAME`
`DATASET_STAGING`
`TABLE_STAGING`
extract_http is not configured to create projects or datasets; it will only create non-existent tables if dataset and project is found.
Therefore `PROJECT_NAME` and `DATASET_STAGING` needs to be changed to reference an existing Project and Dataset respectively.
 
`TABLE_STAGING` supports variable names. If the extraction configuration has key `warehouse` which contains a dict, the value of `TABLE_STAGING` will be formatted against that dictionary to obtain the final name of table.

## Configure /run.sh


## Build the container


# Execution
```Readme WIP```

# Sample Output
 https://datastudio.google.com/reporting/19c15be7-7fba-43b2-bf55-3205db1fd6fa/page/Cl5iC

# Logging
```Readme WIP```
 