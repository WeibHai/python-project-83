import psycopg2 as db
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def insert_in_url_checks(query, url_id, status_code, created_at, title, h1, description):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('i', query)
            cursor.execute(query, (url_id, status_code, created_at, title, h1, description))

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.commit()
            connection.close()
            print('PSQL connection closed.')


def insert_in_urls(query, name, created_at):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('i', query)
            cursor.execute(query, (name, created_at))

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.commit()
            connection.close()
            print('PSQL connection closed.')


def get_one_from_db(query, *args):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('s', query)
            cursor.execute(query, args)
            response = cursor.fetchone()

            print(response)
            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.close()
            print('PSQL connection closed.')


def get_all_from_db(query, *args):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('s', query)
            cursor.execute(query, args)
            response = cursor.fetchall()

            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.close()
            print('PSQL connection closed.')
