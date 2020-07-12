# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

from rpy2 import robjects
from flask import Flask
from flask import request

import subprocess
from flask import jsonify
from rpy2.robjects import pandas2ri
import numpy
import json

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


def is_nd_array(obj):
    if isinstance(obj, numpy.ndarray):
        return obj.tolist()
    else:
        return obj

@app.route('/upload', methods=['POST'])
def upload():
    pandas2ri.activate()
    """Process the uploaded file and upload it to Google Cloud Storage."""
    print(request.form)
    mapper_str: str = request.form['mapper']
    entity = request.form['entity']


    if not mapper_str:
        return 'No file uploaded.', 400

    mapper = robjects.r(mapper_str)
    result = mapper(int(entity))

    print(result)
    # test
    # b = dict(zip(result.names, result[0]))
    # print(b)
    # b = result.tolist()
    # print(b)
    # print(type(b))
    # test end


    # @FIXME this is a workaround, result data shouldn't be processed here
    # but it is somehow required to get result into python data structure from R
    # in order to then send it through REST API - it needs to be in a json parsable form

    # this will probably work only for the one example I attached to the project
    # I think about this as a first attempt to create another language interpreter
    # this needs more investigation

    # possibly we should also send a python function from original project
    # that will convert result data from R function
    data = dict(zip(result.names, entity))

    # this is not working because result[0] is int32 type, not int which
    # makes data object (dict) not processable into json
    # data = dict(zip(result.names, result[0]))
    print(data)

    print("Return string value parsable to json")
    # app_json = json.dumps(data)
    # print(app_json)
    # print(type(app_json))
    return data, 200


@app.route('/upload_reducer', methods=['POST'])
def upload_reducer():
    pandas2ri.activate()
    """Process the uploaded file and upload it to Google Cloud Storage."""
    print(request.form)
    reducer_str: str = request.form['reducer']
    values = request.form['values']
    
    print(values)
    print("HOOO")


    if not reducer_str:
        return 'No file uploaded.', 400

    reducer = robjects.r(reducer_str)
    result = reducer(values)

    print(result)
   
    # data = dict(zip(result.names, entity))

    
    return 200


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=9090, debug=True)
# [END gae_flex_quickstart]
