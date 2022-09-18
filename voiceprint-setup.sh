#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    ./src/cli.py
else
    ./src/cli.py -p "$1"
fi

./src/cli.py -a