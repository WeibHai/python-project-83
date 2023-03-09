import psycopg2 as db
import os
from dotenv import load_dotenv


def send_in_db(query, fetch='all'):

    load_dotenv()

    host = os.getenv("HOST")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    try:
        connection = db.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
            )
        print('PSQL connection.')

        with connection.cursor() as cursor:
            if 'SELECT' in query:
                cursor.execute(query)

                if fetch == 'one':
                    response = cursor.fetchone()

                else:
                    response = cursor.fetchall()

                return response

            elif 'INSERT' in query:
                cursor.execute(query)

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if connection:
            connection.commit()
            connection.close()
            print('PSQL connection closed.')
