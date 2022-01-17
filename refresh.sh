#!/usr/bin/env bash

#######################################################################
### refresh.sh                                                      ###
### Rebuild image, clean up and run the container.                  ###
#######################################################################

# Go to script folder
SELFPATH=$(readlink -f "$0")
SELFDIR=$(dirname "$SELFPATH")

cd $SELFDIR

# Build
./build.sh

# Clean up
../cleanup.sh

# Run
./run.sh "$@"