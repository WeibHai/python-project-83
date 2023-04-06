from bs4 import BeautifulSoup
from page_analyzer.parser import get_description
from page_analyzer.parser import get_title
from page_analyzer.parser import get_h1
import logging
import requests


def get_check(url):
    result = {'status_code': response.status_code}

    soup = BeautifulSoup(response.text, 'html.parser')

    result['description'] = get_description(soup)
    result['title'] = get_title(soup)
    result['h1'] = get_h1(soup)

    return result
