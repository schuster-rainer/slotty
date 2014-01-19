from flask import Flask, render_template, request

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
import gevent

import random
from operator import itemgetter


app = Flask(__name__)
app.config.from_object('slotty.config')
app.config.from_envvar('SLOTTY_CONFIG_FILE')


def read():
    #TODO: add the datalogger data here

    lap_time_estimate = 6.500
    variation = 0.500
    lap_time = random.uniform(lap_time_estimate,
                              lap_time_estimate + 0.100)
    data = []
    for controller in range(6):
        data.append({'lapTime': lap_time,
                     'controller': controller})
        offset = random.uniform(-variation, variation)
        lap_time += offset

    gevent.sleep(lap_time)
    for i in sorted(data, key=itemgetter('lapTime')):
        gevent.sleep(i['lapTime'] - lap_time)
        yield i


class SlottyNamespace(BaseNamespace):
    sockets = {}
    sensing = False

    def recv_connect(self):
        app.logger.info("Client Connected")
        self.sockets[id(self)] = self
        self.loop_sensors()

    def disconnect(self, *args, **kwargs):
        if id(self) in self.sockets:
            app.logger.info("Client %s Disconnected", id(self))
            del self.sockets[id(self)]

    # broadcast to all sockets on this channel!
    @classmethod
    def broadcast(self, event, message):
        for ws in self.sockets.values():
            ws.emit(event, message)

    @classmethod
    def loop_sensors(self):
        if self.sensing:
            return
        self.sensing = True
        while True:
            for race_data in read():
                app.logger.debug(race_data)
                self.broadcast("racetime", race_data)


@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    try:
        socketio_manage(request.environ,
                        {'/slotty': SlottyNamespace},
                        request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)


@app.route('/')
def index():
    return render_template("index.html")
