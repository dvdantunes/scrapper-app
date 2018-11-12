import os
from setuptools import setup, find_packages


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))



description = 'A simple web scraper to parse the web'

long_description = ''
with open(os.path.join(CURRENT_PATH, 'README.md'), 'r') as f:
    long_description = f.read()


requirements = [
        'Flask==1.0.2',
        'Flask-RESTful==0.3.6',
        'service_identity==17.0.0',
        'pyasn1==0.4.4',
        'scrapy==1.5',
        'scrapy-splash==0.7.2',
        'gunicorn==19.9.0',
        'sentry-sdk[flask]==0.5.3',
        'Sphinx==1.8.1',
        'sphinx-rtd-theme==0.4.2',
        'pytest-flask==0.14.0',
        'coverage==4.5.1',
    ]

extras_require = {
    'docs': [
        'Sphinx==1.8.1',
        'sphinx-rtd-theme==0.4.2'
    ],
    'tests': [
        'pytest-flask==0.14.0',
        'coverage==4.5.1',
    ]
}


setup(
    name='kanikumo-engine',
    version='0.4',

    author='David Antunes',
    author_email='dvdantunes@gmail.com',

    url='https://github.com/dvdantunes/scrapper-app',
    project_urls={
        "Source": "https://github.com/dvdantunes/scrapper-app",
        "Tracker": "https://github.com/dvdantunes/scrapper-app/issues",
    },
    description=description,
    long_description=long_description,

    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,

    install_requires=requirements,
    extras_require=extras_require,
)
