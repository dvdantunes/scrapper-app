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


# Run the app
run: install
	FLASK_APP=kanikumo_engine KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/flask run


# Execute test suite
test: install
	KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests


# Builds source to distributable package
sdist: test
	venv/bin/python setup.py sdist
