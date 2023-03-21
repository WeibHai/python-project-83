from flask import flash, url_for, redirect, get_flashed_messages
from flask import Flask, render_template, request
from page_analyzer.connector import send_in_db
from page_analyzer.validator import validate, get_normalization
from page_analyzer.checker import get_check
from dotenv import load_dotenv
from datetime import date
import os


app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def analyzer():
    messages = get_flashed_messages(with_categories=True)

    return render_template('main_page.html', messages=messages)


@app.get('/urls')
def urls():
    query = """SELECT DISTINCT urls.id, urls.name, url_checks.created_at, url_checks.status_code
               FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id ORDER BY urls.id DESC"""

    response = send_in_db(query)

    return render_template('list_urls_page.html', site=response)


@app.route('/urls/<int:id>', methods=['GET', 'POST'])
def url(id):
    messages = get_flashed_messages(with_categories=True)

    query_site = f"""SELECT * FROM urls 
                     WHERE id = {id}"""

    response_site = send_in_db(query_site)

    query_checks = f"""SELECT * FROM url_checks
                       WHERE url_id = {id}
                       ORDER BY id ASC"""

    response_checks = send_in_db(query_checks)

    return render_template(
        'url_page.html',
        messages=messages,
        site=response_site,
        checks=response_checks,
        site_id=id
        )


@app.post('/urls')
def post_analyzer():
    data = request.form.to_dict()

    url = data['url']

    normalizated_url = get_normalization(url)

    errors = validate(normalizated_url)

    if errors:
        for error in errors:
            flash(error, 'error')

        return redirect(url_for('analyzer'))

    query_insert = f'''INSERT INTO urls (name, created_at)
                       VALUES ('{normalizated_url}', '{date.today()}')'''

    send_in_db(query_insert)

    query_select = 'SELECT MAX(id) FROM urls'

    id = send_in_db(query_select, 'one')

    flash('Страница успешно добавлена', 'access')
    return redirect(url_for('url', id=id[0]))


@app.post('/urls/<int:id>/checks')
def post_checks(id):
    query_select = f'''SELECT name FROM urls WHERE id={id}'''

    url = send_in_db(query_select)[0][0]

    try:
        result_check = get_check(url)
    except Exception as _ex:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('url', id=id))

    query_insert = f'''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                       VALUES ('{id}','{result_check['status_code']}', '{result_check['h1']}', '{result_check['title']}', '{result_check['description']}', '{date.today()}')'''

    send_in_db(query_insert)

    flash('Страница успешно проверенна', 'access')
    return redirect(url_for('url', id=id))
