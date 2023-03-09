import validators


def validate(url):
    errors = {}

    if not url:
        errors['existence'] = 'URL обязателен'

    if not validators.url(url):
        errors['validate'] = 'Некорректный URL'
    
    if len(url) > 255:
        errors['size'] = 'URL превышает 255 символов'

    return errors