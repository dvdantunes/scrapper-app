import logging
from flask_restful import Resource

from kanikumo_engine.api.utils import api_response
from kanikumo_engine.libs.scraper import scraper_crawl_job
from kanikumo_engine.libs.scraper.scraper.spiders.mercadopublicocl_alt import MercadoPublicoClBigPurchasesSpiderAlt



class BigPurchasesList(Resource):
    """mercadopublico.cl big purchases api resource

    Get the 20 more recent big purchases data over the last 60 days, from mercadopublico.cl website

    Extends:
        Resource
    """

    def get(self):
        """Get last big purchases from mercadopublico.cl

        Arguments:
            None
        """

        try:
            crawler_response = scraper_crawl_job(MercadoPublicoClBigPurchasesSpiderAlt)
            status = 'success'
            message = crawler_response['message']
            data = crawler_response['data']

        except Exception as e:
            status = 'error'
            data = {}
            message = 'Error while getting data on \'%s\' endpoint' % self.__class__.__name__
            logging.exception(message)


        return api_response(data, status, message)
