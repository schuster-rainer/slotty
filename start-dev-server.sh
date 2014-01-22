#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

export SLOTTY_CONFIG_FILE=$(realpath debug.py)
gunicorn -c server_setup.py slotty.app:app $@
# python slotty/app.py
