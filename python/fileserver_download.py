#!/usr/bin/env python3
# download folder served by https://github.com/chentanyi/fileserver
import os
import bs4
import sys
import base64
import logging
import argparse
import requests
import urllib.parse

try:
    import lxml
    PARSER = 'lxml'
except:
    PARSER = 'html.parser'


def download_file(r: requests.Response, filename: str):
    logging.info(f'Downloading {filename} from {r.url}')
    with open(filename, 'ab+') as fout:
        for content in r.iter_content(chunk_size = 4096):
            fout.write(content)
            fout.flush()


def download_folder(r: requests.Response, filepath: str,
                    sess: requests.Session):
    logging.info(f'Downloading {filepath} from {r.url}')

    html = bs4.BeautifulSoup(r.content, PARSER)
    if not html.title.text.strip().startswith('Index of '):
        logging.warning(f'find html but not folder: {filepath}')
        download_file(r, filepath)
        return

    os.makedirs(filepath, exist_ok = True)

    for tr in html('tr'):
        td = tr.td
        text: str = td.text.strip('/')
        if text == '.' or text == '..':
            logging.debug(f'skip {td}')
            continue

        uri = urllib.parse.urljoin(r.url, td.a['href'])
        path = os.path.join(filepath, text)

        download(uri, path, sess)


def download(uri: str, filepath: str, sess: requests.Session):
    headers = {}
    if os.path.isfile(filepath):
        headers['Range'] = f'bytes={os.stat(filepath).st_size}-'
    r = sess.get(uri, stream = True, headers = headers)
    if r.status_code == 416:
        return
    r.raise_for_status()

    if 'text/html' in r.headers['content-type']:
        download_folder(r, filepath, sess)
    else:
        download_file(r, filepath)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required = True)
    parser.add_argument('-d', '--directory')
    parser.add_argument('-a', '--authorization')
    parser.add_argument('-x', '--proxy')

    return parser.parse_args()


def main():
    args = arg_parse()

    with requests.session() as sess:
        if args.authorization:
            sess.headers[
                'Authorization'] = f'Basic {base64.b64encode(args.authorization.encode()).decode()}'
        if args.proxy:
            sess.proxies = {
                'http': args.proxy,
                'https': args.proxy,
            }

        if not args.directory:
            args.directory = urllib.parse.unquote(
                urllib.parse.urlparse(
                    args.url).path.strip('/').split('/')[-1]) or '.'
        download(args.url, args.directory, sess)


if __name__ == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = "%Y-%m-%d.%H:%M:%S")
    main()