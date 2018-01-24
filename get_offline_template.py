import os
import urllib.request
import urllib.parse


from bs4 import BeautifulSoup


url = 'https://getbootstrap.com/docs/3.3/examples/jumbotron/'


def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return webpage


def get_links_from_html(html, url):
    links = []
    soup = BeautifulSoup(html, 'lxml')

    js_links = soup.find_all('script', {'src': True})
    for js_link in js_links:
        absolute_link_js = urllib.parse.urljoin(url, js_link.get('src'))
        links.append(absolute_link_js)

    css_links = soup.find_all('link', {'href': True})
    for css_link in css_links:
        absolute_link_css = urllib.parse.urljoin(url, css_link.get('href'))
        links.append(absolute_link_css)
    return links


def retrieve_files(links):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    for link in links:
        filename = link.split('/')[-1]
        ext = filename.split('.')[-1]
        save_path = ext + '/' + filename
        if (ext != 'js') and (ext != 'css'):
            continue
        else:
            urllib.request.urlretrieve(link, save_path)


def make_dir():
    dirs = ['js', 'css']
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)


def main():
    make_dir()
    url = 'https://getbootstrap.com/docs/3.3/examples/jumbotron/'
    html = fetch_html(url)
    links = get_links_from_html(html, url)
    retrieve_files(links)


if __name__ == '__main__':
    main()
