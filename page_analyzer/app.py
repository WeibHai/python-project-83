from flask import flash, url_for, redirect, get_flashed_messages
from flask import Flask, render_template, request, make_response
from page_analyzer.validator import validate
from page_analyzer.parser import get_normalization
from page_analyzer.bd import get_one_from_db
from page_analyzer.bd import get_all_from_db
from page_analyzer.bd import presence_in_db
from page_analyzer.bd import insert_in_db
from page_analyzer.check import get_check
from dotenv import load_dotenv
from datetime import date
import os


app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def analyzer():
    return render_template('main_page.html')


@app.get('/urls')
def urls():
    query = '''
            SELECT urls.id, urls.name, url_checks.created_at,
            url_checks.status_code FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            WHERE url_checks.url_id IS NULL
            OR url_checks.id = (SELECT MAX(url_checks.id) FROM url_checks
            WHERE url_checks.url_id = urls.id)
            ORDER BY urls.id DESC
            '''

    response = get_all_from_db(query)

    return render_template('list_urls_page.html', site=response)


@app.route('/urls/<int:id>')
def url(id):
    query_site = """
                 SELECT * FROM urls
                 WHERE id = %s
                 """

    query_checks = """
                   SELECT * FROM url_checks
                   WHERE url_id = %s
                   ORDER BY id DESC
                   """

    response_site = get_all_from_db(query_site, id)
    response_checks = get_all_from_db(query_checks, id)

    return render_template(
        'url_page.html',
        site=response_site,
        checks=response_checks,
        site_id=id
    )


@app.post('/urls')
def post_analyzer():
    data = request.form.to_dict()

    url = data['url']

    normalizated_url = get_normalization(url)

    url_id = presence_in_db(normalizated_url)

    if url_id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url', id=url_id))

    errors = validate(normalizated_url)

    if errors:
        for error in errors:
            flash(error, 'error')

        result = render_template('main_page.html',
                                 saves_url=url)

        return make_response(result, 422)

    query_insert = '''
                   INSERT INTO urls (name, created_at)
                   VALUES (%s, %s)
                   '''

    insert_in_db(query_insert, normalizated_url, date.today())

    query_select = 'SELECT * FROM urls ORDER BY id DESC LIMIT 1'

    response = get_one_from_db(query_select)

    id = response['id']

    flash('Страница успешно добавлена', 'access')
    return redirect(url_for('url', id=id))


@app.post('/urls/<int:id>/checks')
def post_checks(id):
    query_select = '''SELECT * FROM urls WHERE id=%s'''

    response = get_one_from_db(query_select, id)

    result_check = get_check(response['name'])

    if not result_check:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('url', id=id))

    query_insert = '''
                   INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   '''

    insert_in_db(
        query_insert,
        id,
        result_check['status_code'],
        result_check['h1'],
        result_check['title'],
        result_check['description'],
        date.today()
    )

    flash('Страница успешно проверена', 'access')
    return redirect(url_for('url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
