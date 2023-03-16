from bs4 import BeautifulSoup
import requests


def get_check(url):
    result = {}

    response = requests.get('https://' + url)

    soup = BeautifulSoup(response.text, 'html.parser')

    result['status_code'] = response.status_code

    raw_description = soup.find('meta', attrs = {'name': 'description'})

    if raw_description is None:
        result['description'] = 'хуй'
    
    else:
        result['description'] = raw_description.get('content')

    result['title'] = soup.title.string

    h1 = soup.find('h1')

    if h1 is None:
        result['h1'] = ''

    else:
        result['h1'] = h1.text

    return result



    

