from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup

def download_page(url):
    import requests
    try:
        content = requests.get(url).text
        return content
    except:
        print('[ERROR] errors in the url', url)

def get_title(soup):
    if not soup:
        return None
    return soup.find('h2', class_ = 'corner')

def get_month(soup, host):
    title = get_title(soup)

    previousUrl = urljoin(host, title.find('a', class_ = 'l')['href'])
    nextUrl = urljoin(host, title.find('a', class_ = 'r')['href'])

    while title.a:
        title.a.decompose()

    return {
        'title': title.text,
        'previousUrl': previousUrl,
        'nextUrl': nextUrl
    }

def get_dates(soup, host):
    date_list = soup.find_all('dl')
    dict = {}
    for date_item in date_list:
        title = date_item.dt.text
        items = set()

        if not date_item.dd:
            continue

        for a in date_item.find_all('a'):
            items.add(urljoin(host, a['href']))

        dict[title] = items
    return dict

def get_links(url):
    parseResult = urlparse(url)
    host = parseResult[0] + '://' + parseResult[1]

    content = download_page(url)

    soup = BeautifulSoup(content, 'html.parser')
    title_map = get_month(soup, host)
    resource = get_dates(soup, host)

    return {
        'title': title_map['title'],
        'resource': resource,
        'nextUrl': title_map['nextUrl'],
        'previousUrl': title_map['previousUrl']
    }

if __name__ == "__main__":
    inf = get_links('http://www.zmz2019.com/tv/schedule')
    print(inf)
