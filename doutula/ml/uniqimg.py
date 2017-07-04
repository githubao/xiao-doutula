#!/usr/bin/env python
# encoding: utf-8

"""
@description: 获取下载的img的url

@author: BaoQiang
@time: 2017/6/30 20:18
"""

from doutula.pth import FILE_PATH
import json
import hashlib

input_path = '{}/doutu123.json'.format(FILE_PATH)
out_path = '{}/doutu123_image.txt'.format(FILE_PATH)

"""
!sw300st.jpeg
"""

import os


def cnt_sum():
    path = '/data/baoqiang/product/doutu/image'

    file_sum = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))
            print('*' * 30)

        file_sum += len(files)
    print('file len: {}'.format(file_sum))

    dir_sum = 0
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print(os.path.join(root, dir))
            print('*' * 30)
        dir_sum += len(dirs)
    print('dir len: {}'.format(dir_sum))


def process():
    res_set = set()
    with open(input_path, 'r', encoding='utf-8') as f, \
            open(out_path, 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())

            img_urls = json_data['img_urls']
            for item in img_urls:
                res_set.add(item)

        for idx, item in enumerate(res_set, 1):
            dic = {'id': idx, 'img_url': item, 'figure': get_hex(item)}
            json.dump(dic, fw, sort_keys=True, ensure_ascii=False)
            fw.write('\n')


def get_hex(url):
    return hashlib.md5(url.encode()).hexdigest()


def main():
    process()


if __name__ == '__main__':
    main()
