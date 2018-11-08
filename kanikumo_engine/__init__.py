import os
import logging
from flask import Flask

app = Flask(__name__)
app.config.from_object('kanikumo_engine.default_settings')
app.config.from_envvar('KANIKUMO_ENGINE_SETTINGS')


# Logging errors
if os.environ.get('WEB_SERVER') == 'gunicorn':

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

else:
    # Default rotating logs
    from logging.handlers import TimedRotatingFileHandler

    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'kanikumo_engine.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)


import kanikumo_engine.views
