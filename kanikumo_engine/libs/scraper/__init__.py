import os, logging, json
from scrapy import spiderloader, signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.xlib.pydispatch import dispatcher
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor



def scraper_crawl_job(spider_name):
    """Executes an specific spider and returns its crawled results

    The crawling results would be stored into a temporal file that must be read later

    Arguments:
        spider_name {string} -- Spider name

    Returns:
        application/json -- json crawler response
    """


    # Set output file path for spider crawler results
    current_path = os.path.abspath(os.path.dirname(__file__))
    output_file = os.path.join(current_path, 'output.json')

    # Delete results file if exists
    try:
        os.remove(output_file)
    except (OSError, FileNotFoundError) as e:
        # logging.exception("'%s' output_file file not found" % output_file)
        pass



    # Set settings for the crawling process
    crawl_settings = Settings({
        'SPIDER_MODULES': ['kanikumo_engine.libs.scraper.scraper.spiders'],
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0', # valid Firefox 63 UA
        'FEED_FORMAT': 'json',
        'FEED_URI': output_file,
    })



    # Gets the class of the specified spider
    spider_loader = spiderloader.SpiderLoader.from_settings(crawl_settings)

    spider_class = ''
    for name in spider_loader.list():
        if spider_name == name:
            spider_class = spider_loader.load(name)


    # Configure a crawler process for the spider and runs it
    try:

        # Trying to stop reactor
        # @see https://stackoverflow.com/questions/23775915/how-to-know-reactor-is-running-or-not-in-python
        # @see https://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script
        # def reactor_stop():
        #     if reactor.running:
        #         reactor.stop()
        #         logging.info('[scrapy] Reactor stopped')

        # dispatcher.connect(reactor_stop, signal=signals.spider_closed)

        # process = CrawlerProcess(crawl_settings)
        # process.crawl(spider_class)

        # logging.info('[scrapy] Running reactor...')
        # process.start()


        # configure_logging({'LOG_FORMAT': '[%(levelname)s]: %(message)s'})
        # runner = CrawlerRunner(crawl_settings)

        # deferred = runner.crawl(spider_class)
        # deferred.addBoth(lambda _: reactor_stop)
        # if reactor.callWhenRunning(lambda: None) is not None:
        #     logging.info('[scrapy] Running reactor...')
        #     reactor.run()
        # else:
        #     logging.info('[scrapy] Reactor already running ...')

        import requests

        headers={
            'content-type' : 'application/json'
        }
        r = requests.post('http://localhost:8050/execute',
                    json = {
                        "timeout":90,
                        "response_body":False,
                        "images":1,
                        "resource_timeout":60,
                        "save_args":[

                        ],
                        "wait":30,
                        "load_args":{

                        },
                        "viewport":"1024x768",
                        "lua_source":"function main(splash)\r\n  local url = splash.args.url\r\n  assert(splash:go(url))\r\n  assert(splash:wait(1))\r\n\r\n  -- go back 1 month in time and wait a little (1 second)\r\n  assert(splash:runjs(\"document.querySelector('#heaFecha label[for=chkFecha]').click();\"))\r\n  assert(splash:wait(0.2))\r\n\r\n  assert(splash:runjs(\"document.querySelector('#txtFecha1').value = '10-10-2018';\"))\r\n  assert(splash:runjs(\"document.querySelector('#txtFecha2').value = '10-11-2018';\"))\r\n  assert(splash:runjs(\"document.querySelector('#btnBusqueda').click();\"))\r\n  assert(splash:wait(2))\r\n\r\n\r\n  local pages = {}\r\n  pages['1'] = {html = splash:html(), png = splash:png()}\r\n\r\n  assert(splash:runjs(\"document.querySelector('#PaginadorBusqueda__TblPages td:nth-child(3) div').click();\"))\r\n  assert(splash:wait(1))\r\n\r\n  pages['2'] = {html = splash:html(), png = splash:png()}\r\n\r\n  -- return result as a JSON object\r\n  return pages\r\nend",
                        "png":1,
                        "har":1,
                        "html5_media":False,
                        "html":1,
                        "url":"http://www.mercadopublico.cl/Portal/Modules/Site/Busquedas/BuscadorAvanzado.aspx?qs=9",
                        "http_method":"GET",
                        "render_all":False
                    })

        return r.json()

    except Exception as e:
        logging.exception('Error while executing crawling process')
        raise



    # Reads crawler results, process it and return response
    crawler_response = {}
    try:
        with open(output_file, 'r') as f:
            crawler_response = json.loads(f.read())

    except (OSError, FileNotFoundError) as e:
        logging.exception("Error while reading crawler results file: '%s' " % output_file)
        raise


    return crawler_response
