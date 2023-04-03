import validators


def validate(url):
    errors = []

    if not url:
        errors.append('URL обязателен')

    if not validators.url(url):
        errors.append('Некорректный URL')

    if len(url) > 255:
        errors.append('URL превышает 255 символов')

    return errors
