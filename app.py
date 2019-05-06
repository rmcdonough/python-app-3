#!/usr/bin/env python

"""
Example of a painfully trivial Flask application without setting up uWSGI, and
otherwise doing dumb things
"""

import csv
import logging
import json_logging
import os
import random
import redis
import socket
import time
import traceback
import sys
from flask import Flask, jsonify, send_file
from logging.config import dictConfig


app = Flask(__name__)
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init(framework_name='flask')
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

def get_cities():
    results = []
    with open('/cities.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            results.append(row)
    return results


@app.route('/where-is-barret')
def where_is_barret():
    city = (random.choice(get_cities()))
    return jsonify({'where-is-barret': city})


@app.route('/health_check')
def health_check():
    return jsonify({'status': 'ok', 'backend': socket.gethostname()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
