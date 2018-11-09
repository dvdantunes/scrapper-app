import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest



class MercadoPublicoClBigPurchasesSpider(scrapy.Spider):
    """[summary]

    [description]

    Extends:
        scrapy.Spider

    Variables:
        name {str} -- [description]
        start_urls {list} -- [description]
    """
    name = "mercadopublicocl-big-purchases"

    start_urls = ["http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9"]


    def start_requests(self):
        """[summary]

        [description]

        Yields:
            [type] -- [description]
        """

        for url in self.start_urls:
            yield SplashRequest(url=url,
                callback=self.parse,
                endpoint='render.html')



    def parse(self, response):
        """[summary]

        [description]

        Arguments:
            response {[type]} -- [description]
        """

        yield {
            'title' : response.css('title::text').extract_first(),
            'label' : response.css('#heaFecha label[for="chkFecha"]::text').extract_first(),
        }
