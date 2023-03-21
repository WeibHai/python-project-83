from page_analyzer.connector import send_in_db
from urllib.parse import urlparse
import validators


def get_normalization(url):
    raw_result = urlparse(url)
    result = raw_result._replace(path='', params='', query='', fragment='')

    return result.geturl()


def validate(url):
    errors = []
    query = f"SELECT COUNT(*) FROM urls WHERE name = '{url}'"

    if not url:
        errors.append('URL обязателен')

    if not validators.url(url):
        errors.append('Некорректный URL')

    if len(url) > 255:
        errors.append('URL превышает 255 символов')

    if send_in_db(query, 'one')[0] > 0:
        errors.append('Страница уже существует')

    return errors
