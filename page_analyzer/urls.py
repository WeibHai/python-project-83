from urllib.parse import urlparse
import validators


def normalize_url(url):
    raw_result = urlparse(url)
    result = raw_result._replace(path='', params='', query='', fragment='')

    return result.geturl()


def validate(url):
    errors = []

    if url is None:
        errors.append('URL обязателен')
        return errors

    else:
        if not validators.url(url):
            errors.append('Некорректный URL')

        if len(url) > 255:
            errors.append('URL превышает 255 символов')

    return errors
