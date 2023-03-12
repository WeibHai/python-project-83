from flask import flash, url_for, redirect, get_flashed_messages
from flask import Flask, render_template, request
from page_analyzer.connector import send_in_db
from page_analyzer.validator import validate
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import date
import requests
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
    query_urls = "SELECT DISTINCT * FROM urls, url_checks"

    response_urls = send_in_db(query_urls)

    return render_template('list_urls_page.html', site=response_urls)


@app.route('/urls/<id>', methods=['GET', 'POST'])
def url(id):
    messages = get_flashed_messages(with_categories=True)

    query_urls = f"SELECT * FROM urls WHERE id='{id}'"
    query_url_checks = f"SELECT * FROM url_checks WHERE url_id='{id}'"

    response_urls = send_in_db(query_urls)
    response_url_checks = send_in_db(query_url_checks, 'one')

    return render_template('url_page.html', messages=messages,  site=response_urls, checklist=response_url_checks, site_id=id, site_url=response_urls[0][1])


@app.post('/urls')
def post_analyzer():
    data = request.form.to_dict()

    url = data['url']
    netloc = urlparse(url).netloc

    errors = validate(netloc)

    if errors:
        for error in errors:
            flash(error, 'warning')

        return redirect(url_for('analyzer'))

    query_insert = f'''INSERT INTO urls (name, created_at)
                VALUES ('{netloc}', '{date.today()}')'''

    send_in_db(query_insert)

    query_id = f'''SELECT MAX(id) FROM urls'''

    id = send_in_db(query_id, 'one')

    flash('Страница успешно добавлена', 'access')
    return redirect(url_for('url', id=id[0]))


@app.post('/urls/<id>/checks')
def post_checks(id):
    query_id = f'''SELECT name FROM urls WHERE id={id}'''

    url = send_in_db(query_id)

    urlssss = url[0][0]

    try:
        checks_requests = requests.get('https://' + urlssss)

    except Exception as _ex:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('url', id=id))
    
    query_insert = f'''INSERT INTO url_checks (url_id, status_code, created_at)
                           VALUES ('{id}', '{checks_requests.status_code}', '{date.today()}')'''

    send_in_db(query_insert)

    flash('Страница успешно проверенна', 'access')
    return redirect(url_for('url', id=id))
