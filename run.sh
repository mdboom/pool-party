#!/bin/sh -e
rm -rf venv
../cpython/python -m venv venv
venv/bin/pip install git+https://github.com/mdboom/extrainterpreters@main#egg-info=extrainterpreters
venv/bin/pip install gilknocker
time venv/bin/python pool.py $1
