import os
import re
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup


def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return webpage


def get_script_tags(webpage):
    script_tags = re.findall(r'<script\b[^>]*><\/script>', str(webpage))
    return ''.join(script_tags)


def retrieve_js_files(script_tags, url):
    soup = BeautifulSoup(script_tags, 'lxml')
    js_links = soup.find_all('script', {'src': True})
    for js_link in js_links:
        abs_link_js = urllib.parse.urljoin(url, js_link.get('src'))
        filename = abs_link_js.split('/')[-1]
        save_path = 'js/' + filename
        js_link.attrs['src'] = save_path
    try:
        urllib.request.urlretrieve(abs_link_js, save_path)
    except urllib.error.HTTPError as error:
        print("Error while retrieving css files: ", error)


def retrieve_css_files(soup, url):
    css_links = soup.find_all('link', {'rel': 'stylesheet'})
    for css_link in css_links:
        abs_link_css = urllib.parse.urljoin(url, css_link.get('href'))
        filename = abs_link_css.split('/')[-1]
        save_path = 'css/' + filename
        css_link.attrs['href'] = save_path
    try:
        urllib.request.urlretrieve(abs_link_css, save_path)
    except urllib.error.HTTPError as error:
        print("Error while retrieving css files: ", error)


def retrieve_favicion(soup, url):
    favicon = soup.find('link', {'rel': 'icon'})
    favicon_link = favicon.attrs['href']
    abs_favicon_link = urllib.parse.urljoin(url, favicon_link)
    filename = favicon_link.split('/')[-1]
    favicon.attrs['href'] = filename
    try:
        urllib.request.urlretrieve(abs_favicon_link, filename)
    except urllib.error.HTTPError as error:
        print("Error while retrieving favicon: ", error)


def make_dir():
    dirs = ['js', 'css']
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)


def save_index_file(soup):
    with open('index.html', 'w') as file:
        file.write(str(soup.prettify()))


def main():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    make_dir()
    url = 'https://getbootstrap.com/docs/3.3/examples/jumbotron/'
    webpage = fetch_html(url)
    script_tags = get_script_tags(webpage)
    soup = BeautifulSoup(webpage, 'lxml')
    retrieve_js_files(script_tags, url)
    retrieve_css_files(soup, url)
    retrieve_favicion(soup, url)
    save_index_file(soup)


if __name__ == '__main__':
    main()
