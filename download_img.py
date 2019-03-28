import urllib.request 
import shutil
import os
import json
import random
from bs4 import BeautifulSoup
import requests


def download_from_html(html, train_num, test_num):
    shoe_name = html.strip('.html')
    train_dir = os.path.join('train', shoe_name)
    test_dir = os.path.join('test', shoe_name)
    if os.path.exists(train_dir): 
        shutil.rmtree(train_dir)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(train_dir)
    os.makedirs(test_dir)

    with open(os.path.join('htmls', html)) as f:
        webpage = f.read()
        soup = BeautifulSoup(webpage, "lxml")
        tags = soup.findAll(lambda tag:'class' in tag.attrs)
        urls = [json.loads(tag.text)['ou'] for tag in tags if 'rg_meta' in tag['class']]
        random.Random(100).shuffle(urls)
    
    headers = {'User-Agent': 'Mozilla/5.0'} 

    print('Downloading {} training images.'.format(shoe_name))
    for i in range(train_num):
        try:
            r = requests.get(urls[i], headers=headers, timeout=30)
            with open(os.path.join(train_dir, '{}_{}.jpg'.format(shoe_name, i)), 'wb') as f:
                f.write(r.content)
        except requests.exceptions.SSLError:
            print('{} failed!'.format(urls[i]))
            

    print('Downloading {} testing images.'.format(shoe_name))
    for i in range(train_num, train_num+test_num):
        try:
            r = requests.get(urls[i], headers=headers, timeout=30)
            with open(os.path.join(test_dir, '{}_{}.jpg'.format(shoe_name, i)), 'wb') as f:
                f.write(r.content)
        except requests.exceptions.SSLError:
            print('{} failed!'.format(urls[i]))

for html in os.listdir('htmls'):
    train_num = 80
    test_num = 20
    download_from_html(html, train_num, test_num)
