from bs4 import BeautifulSoup


def get_title(soup):
    result = soup.title
    if result is None:
        return ''
    else:
        return result.text


def get_h1(soup):
    result = soup.find('h1')
    if result is None:
        return ''
    else:
        return result.text


def get_description(soup):
    result = soup.find('meta', attrs={'name': 'description'})
    if result is None:
        return ''
    else:
        return result.get('content')


def get_check(url):
    result = {'status_code': 200}

    soup = BeautifulSoup(response.text, 'html.parser')

    result['description'] = get_description(soup)
    result['title'] = get_title(soup)
    result['h1'] = get_h1(soup)

    return result
