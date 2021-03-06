#!/usr/bin/env python
# encoding: utf-8

"""
@description: 线程池下载

@author: BaoQiang
@time: 2017/7/1 10:56
"""

import sys
import time
import os
from doutula.ml.downimg import load_datas
import traceback

from concurrent import futures
import requests

# BASE_PATH = '/mnt/data/baoqiang/product/doutu/image'

BASE_PATH = '/data/baoqiang/product/doutu/image'

timeout = 10


def save_flag(img, filename):
    with open(filename, 'wb') as fw:
        fw.write(img)


def get_flag(url):
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.content
    except Exception as e:
        print(url)
        traceback.print_exc()


MAX_WORKERS = 25


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one,cc_list)

    return len(set(res))


def download_one_test(dic):
    print(dic['id'])
    return dic['img_url']


def download_one(dic):
    if dic['id'] % 1000 == 0:
        print('now process id: {}'.format(dic['id']))
        sys.stdout.flush()

    url = dic['img_url']
    image = get_flag(url)
    if not image:
        print('download {} err'.format(dic['id']))
        return ''

    md5 = dic['finger']
    path = '{}/{}/{}/{}'.format(BASE_PATH, md5[0], md5[1], md5[2])
    if not os.path.exists(path):
        os.makedirs(path)

    posfix = url.split('.')[-1]
    fname = '{}/{}.{}'.format(path, dic['id'], posfix)

    save_flag(image, fname)
    return url


def run():
    t1 = time.time()
    dic_list = load_datas()
    count = download_many(dic_list)
    elasped = time.time() - t1
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elasped))


def main():
    run()


if __name__ == '__main__':
    main()
