import os, scrapy, requests
from scrapy.settings import Settings



class KanikumoCrawler():
    """[summary]

    NOTE: Due to a bug on scrapy-splash on lua scripts execution endpoint, it can't be
    possible to use the standard scrapy-splash approach. Instead, it is used a simple
    http request approach with another Heroku app that deploys the scrapy-splash instance

    NOTE 2: For reference purposes, there is still a copy of the standar scrapy-splash approach
    on paths:
        kanikumo_engine/libs/scraper/__init__.py

    @see Splash won't execute lua script - https://github.com/scrapy-plugins/scrapy-splash/issues/83
    @see AttributeError: 'HtmlResponse' object has no attribute 'data' - https://github.com/scrapy-plugins/scrapy-splash/issues/194


    Extends:
        scrapy.Spider

    Variables:
        start_url {str} -- Url where the crawling begins
        http_method {str} -- HTTP method used when querying the start_url (default: GET)
        lua_source {str} -- LUA scripting file content
        SPLASH_URL {str} -- Splash url endpoint
    """
    start_url = ''

    http_method = 'GET'

    lua_source = ''

    SPLASH_URL = 'https://kanikumo-splash.herokuapp.com/execute'



    def get_lua_source():
        """[summary]

        [description]

        Returns:
            [type] -- [description]
        """
        return self.lua_source



    def crawl(self):
        """[summary]

        [description]

        Returns:
            [type] -- [description]
        """

        # Set settings for the crawling process
        crawl_settings = Settings({
            'SPIDER_MODULES': ['kanikumo_engine.libs.scraper.scraper.spiders'],
            'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0', # valid Firefox 63 UA
        })


        # Set POST data for request
        post_data = {
                    "url": self.start_url,
                    "lua_source": self.get_lua_source(),
                    "http_method": self.http_method,
                    "render_all": False,

                    "wait": 30,
                    "timeout": 90,
                    "response_body": False,
                    "resource_timeout": 90,

                    "save_args":[

                    ],
                    "load_args":{

                    },

                    # "viewport":"1024x768",
                    "html": 1,
                    "images": 1,
                    # "png": 1,
                    # "har": 1,
                    "html5_media": False,
                }

        try:
            response = requests.post(self.SPLASH_URL, json = post_data)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise

        return self.parse(response)


    def parse(self, response):
        """[summary]

        [description]

        Arguments:
            response {[type]} -- [description]

        Returns:
            {str} -- application/json crawler response
        """
        return {}
