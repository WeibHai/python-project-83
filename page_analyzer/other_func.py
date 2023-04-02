from dotenv import load_dotenv
from bs4 import BeautifulSoup
import psycopg2 as db
import logging
import requests
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

LOG_INFO = {
    'c': 'PSQL connection.',
    'd': 'PSQL connection closed.',
    'e': 'Error during check!'}


def insert_in_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(LOG_INFO['c'])

    with connection.cursor() as cursor:
        cursor.execute(query, (args))

        connection.commit()
        connection.close()
        logging.info(LOG_INFO['d'])


def get_one_from_db(query, *args):
    connection = db.connect(DATABASE_URL)

    logging.info(LOG_INFO['c'])

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        response = cursor.fetchone()

        connection.close()
        logging.info(LOG_INFO['d'])

        return response


def get_all_from_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(LOG_INFO['c'])

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        response = cursor.fetchall()

        connection.close()
        logging.info(LOG_INFO['d'])

        return response


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


def get_check(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            result = {'status_code': response.status_code}

            soup = BeautifulSoup(response.text, 'html.parser')

            result['description'] = get_description(soup)
            result['title'] = get_title(soup)
            result['h1'] = get_h1(soup)

            return result

        else:
            raise ('No connection to site')

    except Exception as _ex:
        logging.error(LOG_INFO['e'])
        print('Error during check!', _ex)
        return {}
