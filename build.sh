#!/usr/bin/env bash

#######################################################################
### build.sh                                                        ###
### Rebuild image, clean up and run the container.                  ###
#######################################################################


# Go to script folder
SELFPATH=$(readlink -f "$0")
SELFDIR=$(dirname "$SELFPATH")

cd "$SELFDIR"

# Define name of image and container
IMAGENAME=bigquery_bbc
IMAGEDIR=image


# ./packages fodler is no longer required
# PACKAGEDIR=./packages

# build the image
docker build . --tag $IMAGENAME

# create the image folder
if [ ! -d $IMAGEDIR ]
then
    mkdir $IMAGEDIR
fi

# save a copy of the docker image
# so that it can be deployed to another host if required
docker save -o $IMAGEDIR/$IMAGENAME.tar $IMAGENAME