import os, scrapy, requests
from scrapy.settings import Settings



class KanikumoCrawler():
    """Kanikumo crawler to get data from a specified url site

    Makes a http request with python 'request' api module, parses it response and
    returns the desired data results

    It uses 'splash' as render engine


    NOTE: Due to a bug on scrapy-splash on lua scripts execution endpoint, it cannot be
    possible to use the standard scrapy-splash approach. Instead, it is used a simple
    http request approach with another Heroku app that deploys the scrapy-splash instance

    NOTE 2: For reference purposes, there is still a copy of the standard scrapy-splash approach
    on paths:
        kanikumo_engine/libs/scraper/__init__.py

    @see Splash won't execute lua script - https://github.com/scrapy-plugins/scrapy-splash/issues/83
    @see AttributeError: 'HtmlResponse' object has no attribute 'data' - https://github.com/scrapy-plugins/scrapy-splash/issues/194


    Variables:
        render_url {str} -- Render url endpoint (i.e: splash url)
        start_url {str} -- Url where the crawling should start
        crawler_settings {str} -- Crawler settings
        lua_source {str} -- LUA scripting file content
        lua_source_settings {str} -- LUA script settings
    """
    render_url = 'https://kanikumo-splash.herokuapp.com/execute'

    start_url = ''

    crawler_settings = {}

    lua_source = ''

    lua_source_settings = {}



    def __init__(self):
        """Constructor

        Inits the default lua script and crawler settings
        """
        self.set_lua_source()
        self.set_crawler_settings()



    def set_default_lua_source(self):
        """Set default lua script (a simple html request)

        See splash script documentation:
        @see https://splash.readthedocs.io/en/stable/scripting-tutorial.html
        @see https://splash.readthedocs.io/en/stable/scripting-ref.html

        Returns:
            self
        """
        self.lua_source = """
            function main(splash, args)
              assert(splash:go(args.url))
              assert(splash:wait(0.5))
              return {
                html = splash:html()
              }
            end
            """

        return self



    def set_default_lua_source_settings(self):
        """Set default settings for lua script

        See splash script documentation:
        @see https://splash.readthedocs.io/en/stable/scripting-tutorial.html
        @see https://splash.readthedocs.io/en/stable/scripting-ref.html

        Returns:
            self
        """
        self.lua_source_settings = {
            'js_enabled' : 'true',
            'images_enabled' : 'false',
            'webgl_enabled ' : 'false',
            'media_source_enabled ' : 'false',
            'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0', # valid Firefox 63 UA
        }

        return self



    def set_default_crawler_settings(self):
        """Set default settings for crawler

        See splash script documentation:
        @see https://splash.readthedocs.io/en/stable/api.html

        Returns:
            self
        """
        self.crawler_settings = {
            "url": self.start_url,
            "lua_source": self.get_lua_source(),
            'spider_module': self.__class__.__name__,


            # Heroku free dyno requests can only last up to 30 seconds
            # @see https://help.heroku.com/PFSOIDTR/why-am-i-seeing-h12-request-timeouts-high-response-times-in-my-app
            "timeout": 15,
            "wait": 1,
            "resource_timeout": 5,


            "http_method": 'GET',
            "render_all": 0,
            "viewport":"1024x768",
            "html": 1,
            "images": 0,
            "png": 0,
            "har": 0,
            "html5_media": 0,
            "response_body": 0,
            "save_args":[

            ],
            "load_args":{

            },
        }

        return self



    def get_lua_source_settings(self):
        """Get lua script settings

        Returns:
            dic
        """
        return self.lua_source_settings



    def set_lua_source_settings(self, settings={}, replace=False):
        """Sets lua script settings

        By default, it interpolates the default settings with the specified settings

        Set 'replace' param to True to override all the settings

        See splash script documentation:
        @see https://splash.readthedocs.io/en/stable/scripting-tutorial.html
        @see https://splash.readthedocs.io/en/stable/scripting-ref.html

        Arguments:
            settings {dict} -- Custom dictionary settings [Optional]
            replace {bool} -- Replace with specified settings? [Optional]

        Returns:
            self
        """
        self.set_default_lua_source_settings()
        self.lua_source_settings = {**self.lua_source_settings, **settings} if not replace else settings
        return self



    def get_lua_source(self):
        """Gets lua script

        It takes the specified settings and interpolates them into the lua script

        Returns:
            str
        """
        return self.lua_source % self.get_lua_source_settings()



    def set_lua_source(self, lua_script=''):
        """Sets lua script

        Arguments:
            lua_script {str} -- Lua script

        Returns:
            self
        """
        self.set_default_lua_source_settings()

        if len(lua_script) > 0:
            self.lua_source = lua_script
        else:
            self.set_default_lua_source()

        return self



    def get_crawler_settings(self):
        """Get crawler settings

        Returns:
            dic
        """
        return self.crawler_settings



    def set_crawler_settings(self, settings={}, replace=False):
        """Sets crawler settings

        By default, it interpolates the default settings with the specified settings

        Set 'replace' param to True to override all the settings

        See splash script documentation:
        @see https://splash.readthedocs.io/en/stable/scripting-tutorial.html
        @see https://splash.readthedocs.io/en/stable/scripting-ref.html

        Arguments:
            settings {dict} -- Custom dictionary settings [Optional]
            replace {bool} -- Replace with specified settings? [Optional]

        Returns:
            self
        """
        self.set_default_crawler_settings()
        self.crawler_settings = {**self.crawler_settings, **settings} if not replace else settings

        return self



    def crawl(self):
        """Starts a crawl process and return its parsed results

        In case of error or timeout, it raises a requests.exceptions.RequestException

        Returns:
            str -- Crawler data results
        """
        try:
            response = requests.post(self.render_url, json = self.get_crawler_settings())
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise

        return self.parse(response)



    def parse(self, response):
        """Parses the crawler response and returns the desired data results

        Arguments:
            response {Response} -- Crawler response

        Returns:
            str -- Crawler data results. By default on application/json data type
        """
        return {
            'message' : '',
            'data' : {}
        }
