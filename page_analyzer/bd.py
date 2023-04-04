from dotenv import load_dotenv
import psycopg2 as db
import psycopg2.extras
import logging
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

LOG_MESS = {
    'c': 'PSQL connection.',
    'd': 'PSQL connection closed.'}


def insert_in_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(LOG_MESS['c'])

    with connection.cursor() as cursor:
        cursor.execute(query, (args))

        connection.commit()
        connection.close()
        logging.info(LOG_MESS['d'])


def get_one_from_db(query, *args):
    connection = db.connect(DATABASE_URL)

    logging.info(LOG_MESS['c'])

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        response = cursor.fetchone()

        connection.close()
        logging.info(LOG_MESS['d'])

        return response


def get_all_from_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(LOG_MESS['c'])

    with connection.cursor(cursor_factory=db.extras.DictCursor) as cursor:
        cursor.execute(query, args)
        response = cursor.fetchall()

        connection.close()
        logging.info(LOG_MESS['d'])

        return response


def presence_in_db(url):
    query = f"SELECT COUNT(*) FROM urls WHERE name = '{url}'"

    query_id = f"SELECT id FROM urls WHERE name = '{url}'"

    if get_one_from_db(query)[0] > 0:
        id = get_all_from_db(query_id)[0][0]
        return id

    else:
        return None
