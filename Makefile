PYTHONBIN=python3.6

all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=$(PYTHONBIN) venv && venv/bin/python setup.py develop

run: venv
	FLASK_APP=kanikumo_engine KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/flask run

test: venv
	KANIKUMO_ENGINE_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
