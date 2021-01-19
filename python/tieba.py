#!/usr/bin/env python3
import os
import re
import sys
import logging
import requests
import urllib.parse
from typing import List, Tuple


def fetch_html(url: str, sess: requests.Session) -> Tuple[str, List[str]]:
    r = sess.get(url)
    r.raise_for_status()

    html = r.text
    title = re.findall('<title>([\s\S]*)</title>', html)[0]
    image_urls = re.findall('"(https://imgsa.*?)"', html)
    image_names = [
        urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(u).path))
        for u in image_urls
    ]

    return (title, image_names)


def fetch_pic(title: str, image_names: List[str], sess: requests.Session):
    base_url = 'http://imgsrc.baidu.com/forum/pic/item/'

    if not os.path.exists(title):
        os.makedirs(title)

    for i, image in enumerate(image_names):
        filepath = os.path.join(title, f'{i}.{os.path.splitext(image)[1]}')
        headers = {}
        if os.path.isfile(filepath):
            headers['Range'] = f'bytes={os.stat(filepath).st_size}-'
        url = urllib.parse.urljoin(base_url, image)
        logging.info(f'Fetching {i} {url}')

        r = sess.get(url, headers = headers)
        if r.status_code == 416:
            continue
        r.raise_for_status()

        with open(filepath, 'ab+') as fout:
            fout.write(r.content)


if __name__ == '__main__':
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = "%Y-%m-%d.%H:%M:%S")
    if len(sys.argv) < 2:
        logging.error(f'Usage: {sys.argv[0]} <url>')
        sys.exit(1)

    with requests.session() as sess:
        title, images = fetch_html(sys.argv[1], sess)
        fetch_pic(title, images, sess)