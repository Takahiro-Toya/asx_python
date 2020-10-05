# Download ASX data from https://www.asxhistoricaldata.com/


import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
from urllib.request import Request, urlopen
import ssl
import re
import os
import shutil
import zipfile
import csv
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

zip_download_folder = "./zip_download"
zip_extract_folder = "./extracted"
all_in_one_folder = "./all_in_one"


## 1. Scrape and get all zip file URLs
base_url = "https://www.asxhistoricaldata.com/archive/"
request = Request(base_url, headers={'User-Agent': 'Mozilla/5.0'}) # anything to pass through 403 forbidden
opened = urlopen(request)

try:
    html = opened.read().decode("utf8")
finally:
    opened.close()

targets = re.findall(r'href\="(.+\.zip)', html)

## 2. Download from URLs
def download_url(url, save_path):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request) as zip_file:
        with open(save_path, 'wb') as out_folder:
            out_folder.write(zip_file.read())

for t in targets:
    download_url(t, os.path.join(zip_download_folder, os.path.basename(t)))


# ## 3. Expand files
def expand_file():
    for file in os.listdir(zip_download_folder):
        if (file.endswith(".zip")):
            with zipfile.ZipFile(zip_download_folder + "/" + file, 'r') as zip_ref:
                zip_ref.extractall(zip_extract_folder)

expand_file()


# 4. extract text that exists inside folders and write to csv file

def go_further(current):
    if (os.path.isdir(current)):
        for some in os.listdir(current):
            go_further(current + "/" + some)
    elif (os.path.isfile(current)):
        if (current.endswith(".txt") or current.endswith(".TXT") ):
            df = pd.read_table(current, header=None, delimiter=",")
            df.to_csv('asx_historical_data.csv', index=False, header=False, mode='a')

go_further(zip_extract_folder)



