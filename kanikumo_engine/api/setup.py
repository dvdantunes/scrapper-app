from flask import Flask, Blueprint
from flask_restful import Api

from kanikumo_engine import app
from kanikumo_engine.api.resources.help import Help
from kanikumo_engine.api.resources.mercado_publico import BigPurchasesList


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Help, '/', '/help', strict_slashes=False)
api.add_resource(BigPurchasesList, '/mercadopublico/big-purchases', strict_slashes=False)

app.register_blueprint(api_bp)
