#!/usr/bin/env python
# encoding: utf-8

"""
@description:线程池批量下载图片

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: multidown.py
@time: 2017/1/17 14:34
"""

import threadpool
import threading
from doutula.scrapy.settings import FILE_PATH
import requests
import os
import json

input_file = '{}/biaoqing_item.json'.format(FILE_PATH)
root_path = '{}/img/biaoqing'.format(FILE_PATH)

# pool_size = 50
pool_size = 3


def multi_down():
    datas = load_datas()

    pool = threadpool.ThreadPool(pool_size)
    requests = threadpool.makeRequests(download_image, datas)
    for req in requests:
        pool.putRequest(req)

    pool.poll()
    pool.wait()

    print('task down')


def download_image(dic):
    url = dic['url']
    pid = dic['id']

    response = requests.get(url)

    fname = response.url.split('/')[-1][9:]
    fpath = '{}/{}'.format(root_path, fname[:2])
    if not os.path.exists(fpath):
        os.makedirs(fpath)

    full_path = '{}/{}_{}'.format(fpath, pid, fname)

    with open(full_path, 'wb') as f:
        f.write(response.content)


def load_datas():
    datas = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            dic = None
            try:
                dic = process_line(line)
            except Exception as e:
                print('download img err occur: \t{}\t{}'.format(line, e))

            if dic:
                datas.append(dic)

    return datas


def process_line(line):
    line = line.strip()
    json_data = json.loads(line)

    dic = {}
    dic['id'] = json_data['id']
    dic['url'] = json_data['src_url']

    return dic


def main():
    multi_down()


if __name__ == '__main__':
    main()
