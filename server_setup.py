import os

from gevent import monkey
monkey.patch_all()


def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

#for details have a look at
#http://gunicorn-docs.readthedocs.org/en/latest/settings.html
bind = "0.0.0.0:8000"
workers = 1  # numCPUs() * 2 + 1
backlog = 2048
worker_class = "socketio.sgunicorn.GeventSocketIOWorker"
log_level = "DEBUG"
daemon = False
access_logfile = "-"
error_logfile = "-"

# pidfile ="/tmp/gunicorn.pid"
# logfile ="/tmp/gunicorn.log"
