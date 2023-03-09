import psycopg2 as db
from dotenv import dotenv_values


def send_in_db(query, fetch='all'):

    #host = dotenv_values(".env")['HOST']
    #user = dotenv_values(".env")['USER']
    #password = dotenv_values(".env")['PASSWORD']
    #database = dotenv_values(".env")['DATABASE']

    host = {{HOST}}
    user = {{USER}}
    password = {{PASSWORD}}
    database = {{DATABASE}}

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
