import threading
import urllib.request as urlL
from bs4 import BeautifulSoup
import time

def get_tld(url):
    tld = ''
    dm = url.split('/')[2]
    tld+=dm.split('.')[-2]
    tld+='.'
    tld+=dm.split('.')[-1]
    return tld

ALL = 3
SOME = 2
NONE = 1


class Spider(threading.Thread):
    verbose = SOME
    url = ''
    tld = ''
    crawled = set()
    to_crawl = set()
    FOUND = False

    def get_all_links(page):
        links = []
        soup = BeautifulSoup(page.decode('utf-8', 'ignore'), 'lxml')
        for link in soup.findAll('a'):
            if Spider.tld in link or link['href'].startswith('/'):
                url = link['href']
                if url.startswith('/'):
                    url = Spider.url+link['href']
                links.append(url)

        return links

    def get_page(url):
        try:
            web_p = urlL.urlopen(url)
        except Exception:
            return bytes('')
        return web_p.read()

    def has_file(page):
        soup = BeautifulSoup(page.decode('utf-8', 'ignore'), 'lxml')
        for inpu in soup.findAll('input'):
            if inpu['type'].lower() == 'file':
                return True

        return False

    def __init__(self, main_url, name, _verbose=SOME):
        threading.Thread.__init__(self)
        Spider.url = main_url
        Spider.verbose = _verbose
        self.name = name
        Spider.tld = get_tld(main_url)
        self.i = 0

    def log(self, _str, lvl):
        if self.verbose >= lvl:
             print(_str)
    
    def log_garb(self, _str):
        self.i+=1
        if self.i%(18/self.verbose) == 0:
            print(_str)

    def spi_init(self):
        self.log("[*] Staring the thread "+self.name, SOME)
        links = Spider.get_all_links(Spider.get_page(Spider.url))
        Spider.to_crawl.update(links)

    def stage_2(self):
        for url in Spider.crawled:
            if Spider.has_file(Spider.get_page(url)):
                self.log("\033[0;32m[+] File Upload Found on "+url+'\033[0m' , NONE)
                Spider.FOUND = True

    def run(self):
        self.spi_init()
        s = 0
        self.log('[*] Starting the Main Spider for '+self.name, ALL)
        while True:
            try:
                url = Spider.to_crawl.pop()
                links = Spider.get_all_links(Spider.get_page(url))
                Spider.to_crawl.update(links)
                Spider.crawled.add(url)
                self.log_garb("[i] Crawled "+url)
                s = 0
            except KeyError:
                time.sleep(1)
                if s == 2:
                    break
                s += 1
            
        self.log('[*] Looking for File Uploads', SOME)
        self.stage_2()

        if not Spider.FOUND:
            self.log('[-] We are Sorry to inform you that we were not able to Find any File Upload', NONE)

