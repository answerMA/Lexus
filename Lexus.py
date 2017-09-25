#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/21/2017 2:12 PM
# @Author  : Ruiming_Ma
# @Site    : 
# @File    : Lexus.py
# @Software: PyCharm Community Edition

import requests
from urllib.parse import urlencode
import os
from hashlib import md5


def getHtml(keyword, offset):
    base_url = 'http://www.toutiao.com/search_content/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Host': 'www.toutiao.com',
        'Cookie': 'Cookie:uuid="w:2dabbb6f8fd249509f90383c32af49cd"; tt_webid=6468103577294276110; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=15ea2f8427ec7-00446d783-1f1f4033-1fa400-15ea2f8427f192; __tasessionId=xr5uou7iw1505972738207; CNZZDATA1259612802=147407581-1505970797-%7C1505971588; tt_webid=6468103577294276110',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.toutiao.com/search/?keyword=%E9%9B%B7%E5%85%8B%E8%90%A8%E6%96%AF'
    }

    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }

    try:
        req = requests.get(url=base_url, headers=headers, params=data)
        #print(req.url)
        if req.status_code == 200:
            return req.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def getImage(json):
    n = 0
    if json.get('data'):
        for item in json.get('data'):
            if item.get('tokens') or item.get('cell_type'):
                n = n+1
                #print(n)
            else:
                title = item.get('title')
                images = item.get('image_detail')
                for image in images:
                    yield {
                        'title': title,
                        'image': image.get('url')
                    }


def save_image(item):
    original_path = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\TouTiao\Lexus'
    dir_path = '{0}\{1}'.format(original_path, item.get('title'))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    try:
        response = requests.get(url = item.get('image'))
        if response.status_code == 200:
            file_path = '{0}\{1}.{2}'.format(dir_path, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb+') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError as e:
        print('Error', e.args)

def main():
    for i in range(0, 2):
        html = getHtml('雷克萨斯', i * 20)
        #print('This is %s Page\n' % i)
        for item in getImage(html):
            save_image(item)

    print( '2 pages have been downloaded'+ '\n' )



main()
