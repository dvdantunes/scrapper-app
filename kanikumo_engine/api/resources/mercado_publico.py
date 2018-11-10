import logging
from flask_restful import Resource

from kanikumo_engine.api.utils import api_response
from kanikumo_engine.libs.scraper import scraper_crawl_job



class BigPurchasesList(Resource):
    """mercadopublico.cl big purchases api resource


    Extends:
        Resource
    """
    crawler_name = 'mercadopublicocl-big-purchases'


    def get(self):
        """Get last big purchases from mercadopublico.cl

        Arguments:
            None
        """

        try:
            crawler_response = scraper_crawl_job(self.crawler_name)
            result = 'success'

        except Exception as e:
            logging.exception('Error while crawling "%s" with spider' % self.crawler_name)
            crawler_response = {}
            result = 'error'


        return api_response(crawler_response, result)
