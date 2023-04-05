from dotenv import load_dotenv
import psycopg2 as db
import psycopg2.extras
import logging
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

CONNECT = 'PSQL connection.'

DISCONNECT = 'PSQL connection closed.'


def insert_in_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(CONNECT)

    with connection.cursor() as cursor:
        cursor.execute(query, (args))

        connection.commit()
        connection.close()
        logging.info(DISCONNECT)


def get_one_from_db(query, *args):
    connection = db.connect(DATABASE_URL)

    logging.info(CONNECT)

    with connection.cursor(cursor_factory=db.extras.DictCursor) as cursor:
        cursor.execute(query, args)
        response = cursor.fetchone()

        connection.close()
        logging.info(DISCONNECT)

        return response


def get_all_from_db(query, *args):
    connection = db.connect(DATABASE_URL)
    logging.info(CONNECT)

    with connection.cursor(cursor_factory=db.extras.DictCursor) as cursor:
        cursor.execute(query, args)
        response = cursor.fetchall()

        connection.close()
        logging.info(DISCONNECT)

        return response


def find_in_db(url):
    query = "SELECT * FROM urls WHERE name = %s"

    response = get_one_from_db(query, url)

    if response:
        return response['id']

    else:
        return None
