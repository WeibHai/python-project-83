import psycopg2 as db
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def insert_in_db(query):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('i', query)
            cursor.execute(query)

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.commit()
            connection.close()
            print('PSQL connection closed.')


def get_one_from_db(query):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('s', query)
            cursor.execute(query)
            response = cursor.fetchone()

            print(response)
            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.close()
            print('PSQL connection closed.')


def get_all_from_db(query):
    try:
        connection = db.connect(DATABASE_URL)

        print('PSQL connection.')

        with connection.cursor() as cursor:
            print('s', query)
            cursor.execute(query)
            response = cursor.fetchall()

            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.close()
            print('PSQL connection closed.')
