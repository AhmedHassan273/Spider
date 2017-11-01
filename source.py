import os

# creates a directory
def create_dir(name):
    if not os.path.exists(name):
        print("creating " + name + " directory")
        os.makedirs(name)

# creates queue and crawled files if not created already
def create_data(project, index_url):
    queue = project + '\queue.txt'
    crawled = project + '\crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, index_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# creates no file
def write_file(path, data):
    file = open(path, 'w')
    file.write(data)
    file.close()


# Adds a line of data to an existing file
def append_to_file(path, url):
    with open(url, 'a') as file:
        file.write(url + '\n')


# Deletes all data from an existing file
def empty_file(path):
    with open(path, 'w'):
        pass

# Read a file and convert each line to a set of items
def file_to_set(file_name):
     results = set()
     with open(file_name, 'rt') as f:
        for line in f:
           results.add(line.replace('\n', ''))
     return results


# iterate through a set and put each element in a file each in separate file
def set_to_file(item_set, file):
    empty_file(file)
    with open(file, 'a') as file:
        for item in sorted(item_set):
            file.write(item + '\n')