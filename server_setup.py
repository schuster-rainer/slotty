import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "0.0.0.0:8000"
workers = 1  # numCPUs() * 2 + 1
backlog = 2048
worker_class = "socketio.sgunicorn.GeventSocketIOWorker"
log_level = "DEBUG"
debug = True
daemon = False
access_logfile = "-"
error_logfile = "-"
# pidfile ="/tmp/gunicorn.pid"
# logfile ="/tmp/gunicorn.log"
