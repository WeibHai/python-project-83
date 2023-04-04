from urllib.parse import urlparse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import psycopg2 as db
import psycopg2.extras
import logging
import requests
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

LOG_MESS = {
    'c': 'PSQL connection.',
    'd': 'PSQL connection closed.',
    'e': 'Error during check!'}


def get_title(soup):
    result = soup.title
    if result is None:
        return ''
    else:
        return result.text


def get_h1(soup):
    result = soup.find('h1')
    if result is None:
        return ''
    else:
        return result.text


def get_description(soup):
    result = soup.find('meta', attrs={'name': 'description'})
    if result is None:
        return ''
    else:
        return result.get('content')


def get_normalization(url):
    raw_result = urlparse(url)
    result = raw_result._replace(path='', params='', query='', fragment='')

    return result.geturl()
