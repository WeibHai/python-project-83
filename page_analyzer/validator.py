from page_analyzer.connector import get_one_from_db, get_all_from_db
from urllib.parse import urlparse
import validators


def get_normalization(url):
    raw_result = urlparse(url)
    result = raw_result._replace(path='', params='', query='', fragment='')

    return result.geturl()


def validate(url):
    errors = {}
    query = f"SELECT COUNT(*) FROM urls WHERE name = '{url}'"

    query_id = f"SELECT id FROM urls WHERE name = '{url}'"

    if not url:
        errors['presence_url'] = 'URL обязателен'

    if not validators.url(url):
        errors['valid'] = 'Некорректный URL'

    if len(url) > 255:
        errors['len'] = 'URL превышает 255 символов'

    if get_one_from_db(query)[0] > 0:
        errors['presence_in_db'] = 'Страница уже существует'
        errors['id'] = get_all_from_db(query_id)[0][0]

    return errors
