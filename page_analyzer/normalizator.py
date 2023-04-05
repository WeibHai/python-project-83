from urllib.parse import urlparse


def normalize_url(url):
    raw_result = urlparse(url)
    result = raw_result._replace(path='', params='', query='', fragment='')

    return result.geturl()
