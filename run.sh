#!/bin/bash

echo ">>> Starting screen"
screen -dm bash -c 'FLASK_APP=app.py python3 -m flask run --host=0.0.0.0 --port=80'

