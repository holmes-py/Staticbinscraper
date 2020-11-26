import requests
import re
from bs4 import BeautifulSoup
import os
import multiprocessing

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11'
}

link = f"https://busybox.net/downloads/binaries/1.31.0-i686-uclibc/"


def get_links():
    session = requests.Session()
    response = session.get(link,  headers=headers)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    bin_link = re.finditer(r'<a href="busybox_[A-Z]+">', str(soup))
    name_list = [j.split('"')[1] for j in [i.group(0) for i in bin_link]]
    return name_list


bin_list = get_links()
os.system('mkdir bins;')


def downloader(bin_name):
    os.system(f"wget {link}{bin_name} -O bins/{bin_name.replace('busybox_', '').lower()} &")


pool = multiprocessing.Pool(processes=40)
pool.map(downloader, bin_list)
os.system('chmod +x bins/*')