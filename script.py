import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating the directory '+ directory)
        os.makedirs(directory)

def create_data_files(project_name,base_url):
    queue = os.path.join(project_name,queue.txt)
    crawled = os.path.join(project_name,crawl.txt)
    if not os.path.isfile(queue):
        write_file(queue,base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,'')



def write_file(path,data):
    with open(path,'w') as f:
        f.write(data)

def append_to_file(path,data):
    with open(path,'a') as f:
        f.write(data,'\n')
def delete_file_contents(path):
    open(path,'w').close()



# the file_to_set and set_to_file are for increasing the performance
def file_to_set(file_name):
    result = set()
    with open(file_name, 'rt') as f:
        for line in f :
            result.add(line.replace('\n',''))
    return results

def set_to_file(links,filename):
    with open(filename,'w') as f:
        for l in sorted(link):
            f.write(l+'\n')

