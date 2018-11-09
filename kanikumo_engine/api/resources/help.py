from flask_restful import Resource
from kanikumo_engine.api.utils import output_plaintext


class Help(Resource):
    """Kanikumo engine API help resource

    Extends:
        Resource
    """


    def get(self):
        """Shows Kanikumo engine API help

        Arguments:
            None
        """

        msg = '  _  __           _ _                            _____             _             \n'\
            ' | |/ /__ _ _ __ (_) | ___   _ _ __ ___   ___   | ____|_ __   __ _(_)_ __   ___ \n'\
            ' | \' // _` | \'_ \\| | |/ / | | | \'_ ` _ \\ / _ \\  |  _| | \'_ \\ / _` | | \'_ \\ / _ \\ \n'\
            ' | . \\ (_| | | | | |   <| |_| | | | | | | (_) | | |___| | | | (_| | | | | |  __/ \n'\
            ' |_|\\_\\__,_|_| |_|_|_|\\_\\\\__,_|_| |_| |_|\\___/  |_____|_| |_|\\__, |_|_| |_|\\___| \n'\
            '                                                             |___/  \n'\
            'Kon\'nichiwa! This is Kanikumo Engine scrapper api help. \n\n'\
            'Available end-points: \n'\
            '  /help                             Shows this help \n'\
            '  /mercadopublico/big-purchases     Get last big purchases from mercadopublico.cl \n'

        return output_plaintext(msg)
