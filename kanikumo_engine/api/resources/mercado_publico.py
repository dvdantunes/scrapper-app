import logging
from flask_restful import Resource

from kanikumo_engine.api.utils import api_response
from kanikumo_engine.libs.scraper import scraper_crawl_job
from kanikumo_engine.libs.scraper.scraper.spiders.mercadopublicocl_alt import MercadoPublicoClBigPurchasesSpiderAlt



class BigPurchasesList(Resource):
    """mercadopublico.cl big purchases api resource

    Get 20 more recent big purchases data for the last 60 days, from mercadopublico.cl website

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
            result = 'success'

        except Exception as e:
            logging.exception('Error while getting data on "%s" endpoint' % self.__class__.__name__)
            crawler_response = {}
            result = 'error'


        return api_response(crawler_response, result)
