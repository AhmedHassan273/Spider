from urllib.request import urlopen
from link_finder import LinkFinder
from source import *
from domain import *

class spider:

    base_url = ''
    name = ''
    domain = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, base_url, name, domain_name):
        spider.base_url = base_url
        spider.name = name
        spider.domain = domain_name
        spider.queue_file = spider.name + '/queue.txt'
        spider.crawled_file = spider.name + '/crawled.txt' 
        spider.queue = set()
        spider.crawled = set()
        self.boot()
        self.crawl_page('initial spider', spider.base_url)

    @staticmethod
    def boot():
        create_dir(spider.name)
        create_data(spider.name, spider.base_url)
        spider.queue = file_to_set(spider.queue_file)
        spider.crawled = file_to_set(spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in spider.crawled_file:
            print(thread_name + ' now crawling ' + page_url)
            print('queue has ' + str(len(spider.queue)) + ' items.')
            print('crawled ' + str(len(spider.crawled)) + ' files.')
            spider.AddLinksToQueue(spider.GetLinks(page_url))
            spider.queue.remove(page_url)
            spider.crawled.add(page_url)
            spider.update_files()

    @staticmethod
    def GetLinks(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.getLinks()

    @staticmethod
    def AddLinksToQueue(links):
        for url in links:
            if (url in spider.queue) or (url in spider.crawled):
                continue
            if spider.domain != get_domain(url):
                continue
            spider.queue.add(url)

    @staticmethod
    def update_files():
            set_to_file(spider.queue, spider.queue_file)
            set_to_file(spider.crawled, spider.crawled_file)