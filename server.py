import werkzeug.serving
from socketio import SocketIOServer
from slotty.app import app

@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    port = 8000
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()
