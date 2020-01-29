def download_page(url):
    import requests
    try:
        content = requests.get(url).text
        # print(content)
        return content
    except:
        print(url)

def initial_bs4(content = ''):
    from bs4 import BeautifulSoup
    return BeautifulSoup(content)

if __name__ == "__main__":
    content = download_page('http://www.zmz2019.com/tv/schedule')
    soup = initial_bs4(content)
    for link in soup.find_all('a', title=True):
        print(link)
