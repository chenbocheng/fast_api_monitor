#!/usr/bin/env bash

ROOT_DIR=$(pwd)
TMP_DIR=./tmp
BUILD_PACK=./build/fast_api_monitor.tar.gz

# clean
rm -rf $TMP_DIR
mkdir -p $TMP_DIR
rm -f $BUILD_PACK

# copy files
cp -r ./data $TMP_DIR/data
cp -r ./config $TMP_DIR/config
cp -r ./utils $TMP_DIR/utils
cp -r ./middleware $TMP_DIR/middleware
cp -r ./controller $TMP_DIR/controller
cp -r ./service $TMP_DIR/service
cp -r ./model $TMP_DIR/model
cp -r ./script $TMP_DIR/script
cp ./app.py $TMP_DIR/app.py
cp ./main.py $TMP_DIR/main.py
cp ./requirements.txt $TMP_DIR/requirements.txt

# pack
cd $TMP_DIR && tar -cvf "$ROOT_DIR"/$BUILD_PACK ./*
cd "$ROOT_DIR" && rm -rf $TMP_DIR
