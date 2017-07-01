#!/usr/bin/env python
# encoding: utf-8

"""
@description: 异步io 下载图片

@author: BaoQiang
@time: 2017/7/1 10:31
"""

import sys
import time
import os
from doutula.ml.downimg import load_datas

import asyncio
import aiohttp

BASE_PATH = '/data/baoqiang/product/doutu/image'


def save_flag(img, filename):
    with open(filename, 'wb') as fw:
        fw.write(img)


@asyncio.coroutine
def get_flag(url):
    resp = yield aiohttp.request('GET', url)
    image = yield from resp.read()
    return image


def download_many(dic_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(dic_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)


@asyncio.coroutine
def download_one(dic):
    url = dic['img_url']
    image = yield from get_flag(url)

    md5 = dic['finger']

    path = '{}/{}/{}/{}'.format(BASE_PATH,md5[0],md5[1],md5[2])
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



def main():
    print('do sth')


if __name__ == '__main__':
    main()