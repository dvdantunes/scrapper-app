import os, logging, json
from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess, CrawlerRunner
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
        process = CrawlerProcess(crawl_settings)
        process.crawl(spider_class)
        process.start()

        # configure_logging({'LOG_FORMAT': '[%(levelname)s]: %(message)s'})
        # runner = CrawlerRunner(crawl_settings)

        # deferred = runner.crawl(spider_class)
        # deferred.addBoth(lambda _: reactor.stop())
        # reactor.run()

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
