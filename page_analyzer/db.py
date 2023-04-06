from dotenv import load_dotenv
import psycopg2 as db
import psycopg2.extras
import logging
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

CONNECT_MESSAGE = 'PSQL connection.'

DISCONNECT_MESSAGE = 'PSQL connection closed.'


def insert_in_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(CONNECT_MESSAGE)

    with connection.cursor() as cursor:
        cursor.execute(query, (args))

        connection.commit()
        connection.close()
        logging.info(DISCONNECT_MESSAGE)


def get_one_from_db(query, *args):
    connection = db.connect(DATABASE_URL)

    logging.info(CONNECT_MESSAGE)

    with connection.cursor(cursor_factory=db.extras.DictCursor) as cursor:
        cursor.execute(query, args)
        response = cursor.fetchone()

        connection.close()
        logging.info(DISCONNECT_MESSAGE)

        return response


def get_all_from_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(CONNECT_MESSAGE)

    with connection.cursor(cursor_factory=db.extras.DictCursor) as cursor:
        cursor.execute(query, args)
        response = cursor.fetchall()

        connection.close()
        logging.info(DISCONNECT_MESSAGE)

        return response


def find_in_db(url):
    query = "SELECT * FROM urls WHERE name = %s"

    response = get_one_from_db(query, url)

    if response:
        return response['id']

    else:
        return None
