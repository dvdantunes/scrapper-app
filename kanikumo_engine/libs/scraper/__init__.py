import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from kanikumo_engine.libs.scraper.scraper.spiders.mercadopublicocl import MercadoPublicoClBigPurchasesSpider


def scraper_crawl_job(spider_name):

    current_path = os.path.abspath(os.path.dirname(__file__))
    output_file = os.path.join(current_path, 'output.json')

    settings = get_project_settings()
    crawl_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'FEED_FORMAT': 'json',
        'FEED_URI': output_file,
    }
    settings = {**settings, ** crawl_settings}

    process = CrawlerProcess(settings)
    process.crawl(MercadoPublicoClBigPurchasesSpider)
    process.start()

    crawler_response = {}
    with open(output_file, 'r') as f:
        crawler_response = f.read()

    return crawler_response
