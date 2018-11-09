from flask_restful import Resource

from kanikumo_engine.libs.scraper import scraper_crawl_job



class BigPurchasesList(Resource):
    """mercadopublico.cl big purchases resource


    Extends:
        Resource
    """
    crawler_name = 'mercadopublicocl-big-purchases'


    def get(self):
        """Get last big purchases from mercadopublico.cl

        Arguments:
            None
        """

        crawler_response = {}
        #try:
        crawler_response = scraper_crawl_job(self.crawler_name)

        #except Exception:
        #    pass
            # TODO sentry


        return crawler_response
