#!/usr/bin/env bash

### run.sh
### Run this shell script start the container.
### This keeps it simple, avoiding installation of docker-compose.

# Go to script folder
SELFPATH=$(readlink -f "$0")
SELFDIR=$(dirname "$SELFPATH")


# Define nme of image and container
image_name=bigquery_bbc
container_name=container_${image_name}

# remove existing container if exists
if docker ps -a | grep $container_name > /dev/null; then
    docker rm $container_name > /dev/null
fi

# run the container.
docker run --name $container_name \
    --volume '/opt/bigquery_bim/log:/log' \
    --volume '/opt/bigquery_bim/data:/data' \
    $image_name "$@"