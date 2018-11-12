import os
from datetime import datetime, timedelta
from scrapy.http import Response, HtmlResponse

from kanikumo_engine.libs.scraper.scraper.spiders.kanikumo_crawler import KanikumoCrawler



class MercadoPublicoClBigPurchasesSpiderAlt(KanikumoCrawler):
    """Spider that gets mercadopublico.cl big purchases

    Get (if exists) the 20 more recent big purchases data over the last 60 days, from mercadopublico.cl website

    NOTE: Each page of the results page site contains 10 big purchases


    Extends:
        KanikumoCrawler

    Variables:
        start_url {str} -- Url where the crawling begins
    """
    start_url = "http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9"



    def set_lua_source_settings(self, settings={}, replace=False):
        """Set lua source settings

        Returns:
            self
        """

        # Sets date range to search
        now = datetime.now()
        lua_source_settings = {
            'today' : now.strftime("%d-%m-%Y") if 'today' not in settings else settings['today'],
            'last_60_days' : (now - timedelta(days=60)).strftime("%d-%m-%Y") if 'last_60_days' not in settings \
                                else settings['last_60_days'],
        }

        return super().set_lua_source_settings(lua_source_settings)



    def set_lua_source(self):
        """Sets lua source script

        Returns:
            self
        """
        lua_source = ''

        lua_scripts_path = "%s/lua_scripts/" % os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        filename, file_extension = os.path.splitext(os.path.basename(__file__))
        lua_script_file = os.path.join(lua_scripts_path, '%s.lua' % filename)

        with open(lua_script_file, 'r') as f:
            lua_source = f.read()

        return super().set_lua_source(lua_source)




    def parse(self, response):
        """Parses the crawler response and returns the found data results

        Arguments:
            response {Response} -- Crawler response

        Returns:
            str -- Crawler data results
        """
        response = response.json()


        # Gets data from page 1 (each page has 10 results)
        responsePage1 = HtmlResponse(
                            self.start_url,
                            status=200,
                            body=str.encode(response['page1']['html'])
                        )
        resultsPage1 = self.page_parse(responsePage1)


        # Gets data from page 2
        responsePage2 = HtmlResponse(
                            self.start_url,
                            status=200,
                            body=str.encode(response['page2']['html'])
                        )
        resultsPage2 = self.page_parse(responsePage2)


        # Merge both pages data
        results = resultsPage1 + resultsPage2


        return {
            'message' : 'There were found %d results' % len(results),
            'data' : results
        }




    def page_parse(self, response):
        """Get desired data from page html response

        Arguments:
            response {HtmlResponse} -- HtmlResponse object that contains the html response

        Returns:
            list    Returns the data on a list of dicts, each dict with a particular big purchase data
        """

        def isset(data_list, index):
            return True if len(data_list) > index else False


        results = []
        keys = ['id', 'name', 'buyer', 'supplier', 'invitation_ini_date', 'invitation_end_date', 'status']
        for tableResults in response.css('div#pnlSearch1 table:nth-child(1) tr:not(.cssGridAdvancedResult)'):


            row_data1 = tableResults.css('td a').re(r'.*>(.*)</a>')
            row_data2 = tableResults.css('td span::text').extract()
            row_data = [
                    '' if not isset(row_data1, 0) else row_data1[0],
                    '' if not isset(row_data2, 0) else row_data2[0],
                    '' if not isset(row_data1, 1) else row_data1[1],
                    '' if not isset(row_data1, 2) else row_data1[2],
                    '' if not isset(row_data2, 1) else row_data2[1],
                    '' if not isset(row_data2, 2) else row_data2[2],
                    '' if not isset(row_data2, 3) else row_data2[3],
                ]
            # row_data = row_data1 + row_data2

            big_purchase_row = dict(zip(keys, row_data))
            results.append(big_purchase_row)

        return results


