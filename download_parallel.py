import os
import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


directory = "/path/to/existing/directory"

os.chdir(directory)

urls = []

fns = []

inputs = zip(urls, fns)

def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

t0 = time.time()
for i in inputs:
    result = download_url(i)
    print('url:', result[0], 'time:', result[1])
print('Total time:', time.time() - t0)


def download_parallel(args): 
  cpus = cpu_count() 
  results = ThreadPool(cpus - 1).imap_unordered(download_url, args) 
  for result in results: 
    print('url:', result[0], 'time (s):', result[1])

download_parallel(inputs)
