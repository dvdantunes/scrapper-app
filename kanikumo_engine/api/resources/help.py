from flask_restful import Resource
from kanikumo_engine.api.utils import output_plaintext


class Help(Resource):
    """API help info resource

    Extends:
        Resource
    """


    def get(self):
        """Public mercadopublico.cl API help

        Arguments:
            None
        """

        msg = 'Kon\'nichiwa! This is Kanikumo Engine scrapper api help. \n\n'\
            'Available end-points: \n'\
            '  /help                             Shows this help \n'\
            '  /mercadopublico/big-purchases     Get last big purchases from mercadopublico.cl \n'

        return output_plaintext(msg)
