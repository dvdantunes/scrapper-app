# Kanikumo engine

[![Build Status](https://travis-ci.org/dvdantunes/scrapper-app.svg?branch=master)](https://travis-ci.org/dvdantunes/scrapper-app)


## Overview

A simple web scraper to parse the web


## Demo

You can see Kanikumo engine in action through your browser on its [demo endpoint](https://kanikumo-engine.herokuapp.com/)

Alternatively, you can request it through `curl`. For example:

    $ curl -s https://kanikumo-engine.herokuapp.com/ -v


## Quick Start




## Prerequisites

- Python 3.6
- Flask >= 1.0.2
- Flask-RESTful >= 0.3.6
- scrapy >= 1.5
- scrapy-splash >= 0.7.2

Some important notes:

- This project built to be used with Python 3.6. Update `Makefile` to switch to another python version if needed

- Some dependencies are compiled during installation, so `gcc` and Python header files need to be present.
For example, on Ubuntu:

        $ apt install build-essential python3-dev

- Additionally, you will need to install a `splash` docker container to use its render engine. Please follow the [instructions](https://splash.readthedocs.io/en/stable/install.html) on its official site.

    - After install docker you can pull it from `docker hub`:
        ```$ sudo docker pull scrapinghub/splash```

    - And then start the container:
        ```$ sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash```
        Splash will be available at 0.0.0.0 at port 8050 (http).



## Installation




## Development environment and release process




## Deployment


