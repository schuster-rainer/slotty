from flask import Flask, render_template, request

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import gevent

import random
from operator import itemgetter


app = Flask(__name__)
app.config.from_object('slotty.config')
app.config.from_envvar('SLOTTY_CONFIG_FILE')

fastest_laps = { i: 999.0 for i in range(1,7)}
laps = { i: 0 for i in range(1,7)}

def read():
    global fastest_laps
    global laps

    lap_time_estimate = 6.500
    variation = 0.500
    lap_time = random.uniform(lap_time_estimate,
                              lap_time_estimate + 0.100)
    data_list = []
    for controller in range(1,7):
        laps[controller] += 1
        fastest = fastest_laps[controller]
        data = {'lapTime': lap_time,
                'controller': controller,
                'lapTimeFastest': fastest,
                'laps': laps[controller]}
        offset = random.uniform(-variation, variation)
        if lap_time < fastest:
            data["lapTimeFastest"] = lap_time
            fastest_laps[controller] = lap_time
        data_list.append(data)
        lap_time += offset

    gevent.sleep(lap_time)
    for i in sorted(data_list, key=itemgetter('lapTime')):
        gevent.sleep(i['lapTime'] - lap_time)
        yield i


class SlottyNamespace(BaseNamespace, BroadcastMixin):
    sensing = False

    def recv_connect(self):
        app.logger.info("Client Connected")
        self.loop_sensors()

    def disconnect(self, *args, **kwargs):
        app.logger.info("Client Disconnected", id(self))

    def loop_sensors(self):
        if self.sensing:
            return
        self.sensing = True
        while True:
            for race_data in read():
                app.logger.debug(race_data)
                self.broadcast_event("racetime", race_data)


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
