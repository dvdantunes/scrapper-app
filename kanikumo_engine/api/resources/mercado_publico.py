from flask_restful import Resource



class BigPurchasesList(Resource):
    """mercadopublico.cl big purchases resource


    Extends:
        Resource
    """

    def get(self):
        """Get last big purchases from mercadopublico.cl

        Arguments:
            None
        """

        return {}
