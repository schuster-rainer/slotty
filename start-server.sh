#!/bin/bash
gunicorn -k flask_sockets.worker webrms.gui.app:app $@
