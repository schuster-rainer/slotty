virtualenv .venv
.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
