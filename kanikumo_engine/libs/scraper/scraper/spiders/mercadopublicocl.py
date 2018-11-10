import os, scrapy
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

        script = """
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

          return pages
        end
        """ % ('10-10-2018', '10-11-2018')


        # yield SplashRequest('http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9',
        #     self.parse,
        #     args={
        #         # time to wait for updates after page is loaded
        #         # 'wait' : 50,

        #         # 'timeout' : 60,
        #         'lua_source': script
        #     },
        #     cache_args=['lua_source'],
        #     endpoint='execute')


        yield scrapy.Request('http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9',
            self.parse,
            meta={
                'splash': {
                    "args":{
                        # time to wait for updates after page is loaded
                        "timeout":90,
                        "response_body":False,
                        "images":1,
                        "resource_timeout":0,
                        "save_args":[

                        ],
                        "wait":30,
                        "load_args":{

                        },
                        "viewport":"1024x768",
                        'lua_source': script,
                        "png":1,
                        "har":1,
                        "html5_media":False,
                        "html":1,
                        "url":"http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9",
                        "http_method":"GET",
                        "render_all":False
                    },
                    'cache_args':['lua_source'],
                    'endpoint':'execute'
                },
            },
        )



    def parse(self, response):
        """[summary]

        [description]

        Arguments:
            response {[type]} -- [description]
        """

        # current_path = os.path.abspath(os.path.dirname(__file__))
        # output_file = os.path.join(current_path, 'output2.json')

        # with open(output_file, "w+") as text_file:
        #     text_file.write(response.body_as_unicode())
        #     pass

        yield {
            'data' : response.data
        }
