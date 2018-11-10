from scrapy.http import Response, HtmlResponse

from kanikumo_engine.libs.scraper.scraper.spiders.kanikumo_crawler import KanikumoCrawler



class MercadoPublicoClBigPurchasesSpiderAlt(KanikumoCrawler):
    """Spider that gets mercadopublico.cl big purchases

    Get 20 more recent big purchases data for the last 60 days, from mercadopublico.cl website

    To know more about the selected request approach, please review the docs of the following files:
        @see kanikumo_engine/libs/scraper/scraper/spiders/kanikumo_crawler.py
        @see kanikumo_engine/libs/scraper/scraper/spiders/mercadopublicocl.py

    Extends:
        KanikumoCrawler

    Variables:
        start_url {str} -- Url where the crawling begins
    """

    start_url = "http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9"



    def get_lua_source(self):

        self.lua_source = """
        function main(splash)
          local url = splash.args.url
          assert(splash:go(url))
          assert(splash:wait(1))

          -- set dates and submit form
          assert(splash:runjs("document.querySelector('#heaFecha label[for=chkFecha]').click();"))
          assert(splash:wait(0.2))

          assert(splash:runjs("document.querySelector('#txtFecha1').value = '%s';"))
          assert(splash:runjs("document.querySelector('#txtFecha2').value = '%s';"))
          assert(splash:runjs("document.querySelector('#btnBusqueda').click();"))
          assert(splash:wait(3))

          -- get pages content
          local pages = {}
          pages['page1'] = {html = splash:html()}

          -- check paginator #2 and get page 2
          assert(splash:runjs("document.querySelector('#PaginadorBusqueda__TblPages td:nth-child(3) div').click();"))
          assert(splash:wait(3))
          pages['page2'] = {html = splash:html()}

          --return {title = splash:evaljs("document.title")}
          return pages
        end
        """ % ('10-10-2018', '10-11-2018')

        return self.lua_source




    def parse(self, response):
        """[summary]

        [description]

        Arguments:
            response {[type]} -- [description]

        Returns:
            {str} -- application/json crawler response
        """

        response = response.json()

        responsePage1 = HtmlResponse(
                            self.start_url,
                            status=200,
                            body=str.encode(response['page1']['html'])
                        )

        responsePage2 = HtmlResponse(
                            self.start_url,
                            status=200,
                            body=str.encode(response['page2']['html'])
                        )

        return {
            "title1": responsePage1.css('title::text').extract_first().strip(),
            "title2": responsePage2.css('title::text').extract_first().strip()
        }
