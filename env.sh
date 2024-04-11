#!/bin/sh

PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD 1> /dev/null 2>&1
then
    echo "$PYTHON_CMD could not be found"
    exit 1
fi

mkdir .venv > /dev/null 2>&1

if ! $PYTHON_CMD -m venv .venv
then
    echo Unable to set up venv
    exit 1
fi
if ! source .venv/bin/activate > /dev/null 2>&1
then
    if ! . .venv/bin/activate > /dev/null 2>&1
    then
        echo Unable to set source
        exit 1
    fi
fi
python3 -m pip install -r requirements.txt

echo Successfully initialized environment and installed all dependencies.
