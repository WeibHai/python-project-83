from bs4 import BeautifulSoup
import requests


def get_check(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:

            result = {}

            soup = BeautifulSoup(response.text, 'html.parser')

            result['status_code'] = response.status_code

            raw_description = soup.find('meta', attrs={'name': 'description'})

            if raw_description is None:
                result['description'] = ''
            
            else:
                result['description'] = raw_description.get('content')

            title = soup.title

            if title is None:
                result['title'] = ''
            else:
                result['title'] = title.string

            h1 = soup.find('h1')

            if h1 is None:
                result['h1'] = ''

            else:
                result['h1'] = h1.text
            
            return result

    except Exception as _ex:
        result = {}
        print('Error while working with PSQL', _ex)
        return result
