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

        # Get date range to search
        today = '10-11-2018'
        last_60_days = '10-10-2018'


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
        """ % (last_60_days, today)

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
        resultsPage1 = self.page_parse(responsePage1)


        responsePage2 = HtmlResponse(
                            self.start_url,
                            status=200,
                            body=str.encode(response['page2']['html'])
                        )
        resultsPage2 = self.page_parse(responsePage2)


        return resultsPage1 + resultsPage2


    def page_parse(self, response):

        results = []
        keys = ['id', 'name', 'buyer', 'supplier', 'invitation_ini_date', 'invitation_end_date', 'status']
        for tableResults in response.css('div#pnlSearch1 table:nth-child(1) tr:not(.cssGridAdvancedResult)'):

            row_data1 = tableResults.css('td a').re(r'.*>(.*)</a>')
            row_data2 = tableResults.css('td span::text').extract()
            row_data = [
                    row_data1[0],
                    row_data2[0],
                    row_data1[1],
                    row_data1[2],
                    row_data2[1],
                    row_data2[2],
                    row_data2[3],
                ]
            # row_data = row_data1 + row_data2

            big_purchase_row = dict(zip(keys, row_data))
            results.append(big_purchase_row)

        return results


