from flask import flash, url_for, redirect
from flask import Flask, render_template, request
from page_analyzer.urls import validate
from page_analyzer.urls import normalize_url
from page_analyzer.db import get_one_from_db
from page_analyzer.db import get_all_from_db
from page_analyzer.db import find_in_db
from page_analyzer.db import insert_in_db
from page_analyzer.check import get_check
from dotenv import load_dotenv
from datetime import date
import requests
import os


app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def analyzer():
    return render_template('main.html')


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

    return render_template('list_urls.html', site=response)


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

    response_site = get_one_from_db(query_site, id)
    response_checks = get_all_from_db(query_checks, id)

    return render_template(
        'url.html',
        site=response_site,
        checks=response_checks,
        site_id=id
    )


@app.post('/urls')
def post_analyzer():
    data = request.form.to_dict()

    url = data['url']

    normalized = normalize_url(url)

    url_id = find_in_db(normalized)

    if url_id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url', id=url_id))

    errors = validate(normalized)

    if errors:
        for error in errors:
            flash(error, 'danger')

        return render_template('main.html', url_name=url), 422

    query_insert = '''
                   INSERT INTO urls (name, created_at)
                   VALUES (%s, %s)
                   '''

    insert_in_db(query_insert, normalized, date.today())

    query_select = 'SELECT * FROM urls ORDER BY id DESC LIMIT 1'

    response = get_one_from_db(query_select)

    id = response['id']

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url', id=id))


@app.post('/urls/<int:id>/checks')
def post_checks(id):
    query_select = '''SELECT * FROM urls WHERE id=%s'''

    url = get_one_from_db(query_select, id)['name']

    result_check = requests.get(url)

    if result_check.status_code != 200:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url', id=id))
    
    else:
        get_check(result_check)

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

        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
