#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

export SLOTTY_CONFIG_FILE=$(realpath debug.cfg)
gunicorn -k socketio.sgunicorn.GeventSocketIOWorker slotty.app:app --log-level debug --access-logfile - --error-logfile - $@

