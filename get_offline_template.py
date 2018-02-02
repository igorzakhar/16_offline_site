import os
import re
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup, Comment
from html5print import HTMLBeautifier


def fetch_html(url):
    req = urllib.request.Request(url)
    webpage = urllib.request.urlopen(req).read()
    return webpage


def get_comment_out_links(soup, url):
    script_tags = []
    pattern = re.compile(r'<script\b[^>]*><\/script>')
    js_links = soup.find_all(text=lambda text: isinstance(text, Comment))
    for js_link in js_links:
        match = re.findall(pattern, js_link.string)
        if match:
            script_tags.extend(match)
    soup = BeautifulSoup(''.join(script_tags), 'lxml')
    comment_out_links = get_js_links(soup, url)
    return comment_out_links, script_tags


def get_js_links(soup, url):
    abs_links = []
    js_links = soup.find_all('script', {'src': True})
    for js_link in js_links:
        abs_link_js = urllib.parse.urljoin(url, js_link.get('src'))
        abs_links.append(abs_link_js)
        filename = abs_link_js.split('/')[-1]
        save_path = 'js/{}'.format(filename)
        js_link.attrs['src'] = save_path
    return abs_links


def get_css_links(soup, url):
    abs_links = []
    css_links = soup.find_all('link', {'rel': 'stylesheet'})
    for css_link in css_links:
        abs_link_css = urllib.parse.urljoin(url, css_link.get('href'))
        filename = abs_link_css.split('/')[-1]
        save_path = 'css/{}'.format(filename)
        css_link.attrs['href'] = save_path
        abs_links.append(abs_link_css)
    return abs_links


def get_favicon_link(soup, url):
    favicon = soup.find('link', {'rel': 'icon'})
    favicon_link = favicon.attrs['href']
    abs_favicon_link = urllib.parse.urljoin(url, favicon_link)
    filename = favicon_link.split('/')[-1]
    favicon.attrs['href'] = filename
    return abs_favicon_link


def retrieve_js_files(js_links):
    for js_link in js_links:
        save_path = 'js/{}'.format(js_link.split('/')[-1])
        try:
            urllib.request.urlretrieve(js_link, save_path)
        except urllib.error.HTTPError as error:
            continue


def retrieve_css_files(css_links):
    for css_link in css_links:
        save_path = 'css/{}'.format(css_link.split('/')[-1])
        try:
            urllib.request.urlretrieve(css_link, save_path)
        except urllib.error.HTTPError as error:
            continue


def retrieve_favicion(favicon_link):
    filename = favicon_link.split('/')[-1]
    try:
        urllib.request.urlretrieve(favicon_link, filename)
    except urllib.error.HTTPError as error:
        return


def make_directories():
    directories = ['js', 'css']
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)


def save_index_file(html):
    with open('index.html', 'w') as file:
        file.write(HTMLBeautifier.beautify(html))


def replace_comment_out_links(soup, tags, url):
    html = str(soup)
    script_soup = BeautifulSoup(''.join(tags), 'lxml')
    script_tags = script_soup.find_all('script')
    for tag in script_tags:
        replace_path = 'js/{}'.format(tag.attrs['src'].split('/')[-1])
        replace_string = '<script src="{}"></script>'.format(replace_path)
        html = html.replace(str(tag), replace_string)
    return html


def main():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    make_directories()
    url = 'https://getbootstrap.com/docs/3.3/examples/jumbotron/'

    webpage = fetch_html(url)
    soup = BeautifulSoup(webpage, 'lxml')

    js_links = get_js_links(soup, url)
    comment_out_links, script_tags = get_comment_out_links(soup, url)
    all_js_links = [*js_links, *comment_out_links]
    retrieve_js_files(all_js_links)

    css_links = get_css_links(soup, url)
    retrieve_css_files(css_links)

    favicon_link = get_favicon_link(soup, url)
    retrieve_favicion(favicon_link)

    html = replace_comment_out_links(soup, script_tags, url)

    save_index_file(html)


if __name__ == '__main__':
    main()
