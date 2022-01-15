#!/usr/bin/env bash

IMAGENAME=bigquery_bbc
SELFPATH=$(readlink -f "$0")
SELFDIR=$(dirname "$SELFPATH")
IMAGEDIR=image

cd "$SELFDIR"

PACKAGEDIR=./packages

cp -r ~/Documents/RandPython/Credentials/BigQuery/bim-manufacturer-metadata/api-injection ./credentials

# cp /usr/include/asm-generic/socket.h ./app
docker build . --tag $IMAGENAME



if [ ! -d $IMAGEDIR ]
then
    mkdir $IMAGEDIR
fi

docker save -o $IMAGEDIR/$IMAGENAME.tar $IMAGENAME