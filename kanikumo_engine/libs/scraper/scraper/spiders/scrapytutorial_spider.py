import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest


class QuotesSpider(scrapy.Spider):
    """[summary]

    [description]

    Extends:
        scrapy.Spider

    Variables:
        name {str} -- [description]
        start_urls {list} -- [description]
    """
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]


    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }



class QuotesJSSpider(scrapy.Spider):
    """[summary]

    [description]

    Extends:
        scrapy.Spider

    Variables:
        name {str} -- [description]
        start_urls {list} -- [description]
    """
    name = "quotes-js"

    start_urls = ["http://quotes.toscrape.com/js/"]


    def start_requests(self):
        """[summary]

        [description]

        Yields:
            [type] -- [description]
        """

        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')


    def parse(self, response):
        """[summary]

        [description]

        Arguments:
            response {[type]} -- [description]
        """

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
