import gevent
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

import zmq.green as zmq
from pkg_resources import iter_entry_points


class Slotty(Flask):
    """ Flask app collecting all ioloop
    extensions points """

    def __init__(self, *args, **kwargs):
        super(Slotty, self).__init__(*args, **kwargs)
        self.config.from_object('slotty.config')
        self.config.from_envvar('SLOTTY_CONFIG_FILE')
        self.load_sensors()

    def load_sensors(self):
        """ Loads all entry points for the sensors.

        The entry point must return a function. The function is
        passed the zmq.green address to bind against for pushing
        the notifications. The notifications are forwarded to
        all connected clients through a socket.io connection.
        The sensor has to use gevent.sleep() to yield to other
        cooperative green threads. The
        """
        for entry_point in iter_entry_points(group='slotty.publisher', name=None):
            sensor = entry_point.load()
            gevent.spawn(sensor, self.config["API_ADDRESS"])


class SlottyAPI(BaseNamespace, BroadcastMixin):
    """ Endpoint for the socket.io connection.

    Broadcasts all incoming zmq.green data to the connected
    clients
    """
    def recv_connect(self):
        context = zmq.Context()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect(app.config["API_ADDRESS"])
        app.logger.info("API router connected, ready to stream...")
        while True:
            data = sock.recv_json()
            app.logger.debug(data)
            self.broadcast_event(data["event"], data["args"])
            gevent.sleep(0.1)


app = Slotty(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    try:
        socketio_manage(request.environ,
                        {'/sensors': SlottyAPI},
                        request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
