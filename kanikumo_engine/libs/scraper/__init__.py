import os, logging, json


def scraper_crawl_job(spider_class):
    """Executes the specified spider and returns its crawled results

    NOTE: Due to a bug on scrapy-splash on lua scripts execution endpoint, it cannot be
    possible to use the standard scrapy-splash approach. Instead, it is used a simple
    http request approach with another Heroku app that deploys the scrapy-splash instance

    NOTE 2: For reference purposes, there is still a copy of the standard scrapy-splash approach
    on paths:
        kanikumo_engine/libs/scraper/__init__.py

    @see Splash won't execute lua script - https://github.com/scrapy-plugins/scrapy-splash/issues/83
    @see AttributeError: 'HtmlResponse' object has no attribute 'data' - https://github.com/scrapy-plugins/scrapy-splash/issues/194


    Arguments:
        spider_class {KanikumoCrawler} -- Spider class

    Returns:
        {str} -- application/json crawler response
    """


    # Configure the spider and runs it
    try:
        spider = spider_class()
        crawler_response = spider.crawl()

    except Exception as e:
        logging.exception('Error while executing crawling process')
        raise

    return crawler_response

