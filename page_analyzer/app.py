from flask import Flask, render_template, request
from flask import flash, url_for, redirect, get_flashed_messages
from urllib.parse import urlparse
from page_analyzer.validator import validate
from page_analyzer.connector import send_in_db
from datetime import date
from dotenv import dotenv_values


app = Flask(__name__)

 #app.config['SECRET_KEY'] = dotenv_values(".env")['SECRET_KEY']
app.config['SECRET_KEY'] = {{'SECRET_KEY'}}


@app.route('/')
def analyzer():
    messages = get_flashed_messages(with_categories=True)

    return render_template('main_page.html', messages=messages)


@app.get('/urls')
def urls():
    query = "SELECT * FROM urls ORDER BY created_at DESC"

    response = send_in_db(query)

    return render_template('list_urls_page.html', list_urls=response)


@app.get('/urls/<id>')
def url(id):
    #messages = get_flashed_messages(with_categories=True)

    query = f"SELECT * FROM urls WHERE id='{id}'"

    response = send_in_db(query)

    return render_template('url_page.html', site=response)


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

    query = f'''INSERT INTO urls (name, created_at)
                VALUES ('{netloc}', '{date.today()}')'''

    send_in_db(query)

    flash('Страница успешно добавлена', 'access')
    return redirect(url_for('urls'))
