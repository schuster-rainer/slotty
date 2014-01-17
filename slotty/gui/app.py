from flask import Flask, jsonify, render_template
import json
from flask.ext.sockets import Sockets
from webrms import datalogger

app = Flask(__name__)
sockets = Sockets(app)


# def ws_url_builder(error, endpoint, values):
#     if endpoint != 'ws':
#         return
#     filename = values.pop('filename')
#     sever_name = values.pop('_external')
#     return '%s/%s%s' % (
#         server_name,
#         filename,
#         values and '?' + url_encode(values) or '',
#     )

# app.url_build_error_handlers.append(ws_url_builder)



@sockets.route('/datalogger')
def datalogger_socket(ws):
    while True:
        for race_data in datalogger.read():
            print race_data
            #TODO: either return data from read
            # read shouldn't return the raw sensor data
            # from the Control Unit. Define some
            # usefull interface
            # as python dict or something equivalent
            # Dictionary Example:
            # { 'car' : 1,
            #   'time' : 23.000,
            # }
            message = json.dumps(race_data)
            ws.send(message)


@app.route('/')
def index():
    return render_template("index.html")
