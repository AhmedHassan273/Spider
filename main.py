import threading
from queue import Queue
from Spider import spider
from domain import *
from source import *

Project_Name = '' # Name of The Directory (input)
home_page = '' # Home Page of The Site You Want to Crawl (input)
domain_name = get_domain(home_page)
queue_file = Project_Name + '/queue.txt'
crawled_file = Project_Name + '/crawled.txt'
number_of_threads = 8
thread_queue = Queue()
spider(home_page, Project_Name, domain_name)

def create_workers():
    for x in range(number_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = thread_queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()

def create_jobs():
    for link in file_to_set(queue_file):
        thread_queue.put(link)
    thread_queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()