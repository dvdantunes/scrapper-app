# Python binary path. Change it if you need to work with another python version
PYTHONBIN=python3.6



# Default rule
all: run


# Remove virtualenv and installed deployment files
clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*


# Create virtualenv with defined python version
venv:
	virtualenv --python=$(PYTHONBIN) venv


# Install the app with setuptools approach
install: venv
	venv/bin/python setup.py develop


# Run the app on development env
run-dev: install
	WEB_SERVER=flask-wsgi FLASK_APP=kanikumo_engine KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/flask run


# Run the app on production env
run: install
	WEB_SERVER=gunicorn FLASK_APP=kanikumo_engine KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/gunicorn kanikumo_engine:app -p /tmp/kanikumo_engine.pid -b 127.0.0.1:5000 --access-logfile logs/access.log --log-file logs/error.log -D

# Stop the app
stop:
	kill `cat /tmp/kanikumo_engine.pid`


# Execute test suite
test: install
	KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests


# Builds source to distributable package
sdist: test
	venv/bin/python setup.py sdist
