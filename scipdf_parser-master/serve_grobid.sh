#!/bin/bash

# download GROBID if directory does not exist
declare -r GROBID_VERSION="0.6.2" # or change to current stable version

if [ ! -d grobid-${GROBID_VERSION} ]; then
  wget https://github.com/kermitt2/grobid/archive/${GROBID_VERSION}.zip
  unzip "${GROBID_VERSION}.zip"
  rm "${GROBID_VERSION}.zip"
fi

# run GROBID
cd grobid-${GROBID_VERSION} || exit
./gradlew run
