#!/bin/sh -e
rm -rf venv
../cpython/python -m venv venv
venv/bin/pip install -e ../extrainterpreters/
venv/bin/pip install gilknocker
/usr/bin/time venv/bin/python pool.py $1
