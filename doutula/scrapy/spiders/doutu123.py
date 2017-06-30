#!/usr/bin/env python
# encoding: utf-8

"""
@description: doutu123 斗图神器 的爬虫

@author: BaoQiang
@time: 2017/6/30 11:02
"""

import json

import requests
import scrapy
from scrapy.http import FormRequest

from doutula.scrapy.items import Doutu123Item
from doutula.scrapy.settings import FILE_PATH

out_file = '{}/doutu123.json'.format(FILE_PATH)
url_fmt = 'http://mobile.doutu123.com/news/?last_id={}'

headers = {
    'ticket': 'xUSfLshuWc7tmVLqGfynGE'
}


class Doutu123Spider(scrapy.Spider):
    name = 'doutu123_spider'
    allow_domins = ['doutu123.com']

    processed_id = set()

    def start_requests(self):
        return [FormRequest('http://mobile.doutu123.com/news/', callback=self.parse_list, headers=headers)]

    def parse_list(self, response):
        for i in range(1, 100000001):
            yield FormRequest(url_fmt.format(i), callback=self.parse_item, headers=headers)

    def parse_item(self, response):
        data = response.body.decode()
        json_data = json.loads(data)

        # print(json_data)

        res_lst = []
        try:
            for item in json_data['news']:
                doutu = Doutu123Item()

                doutu['url'] = item['furl']
                uid = item['id']

                if 'source_data' in item and 'name' in item['source_data']:
                    doutu['desc'] = item['source_data']['name']
                else:
                    doutu['desc'] = ''

                if uid not in self.processed_id:
                    res_lst.append(doutu)
                    self.processed_id.add(uid)
                    doutu['id'] = uid

        except Exception as e:
            print('ERROR: {}'.format(json_data))

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in res_lst:
                fw.write('{}\n'.format(item))

        for item in res_lst:
            yield FormRequest(url_fmt.format(item['id']), callback=self.parse_item, headers=headers)


def test():
    url = 'http://mobile.doutu123.com/news/?last_id=82182416'
    response = requests.get(url, headers=headers)
    print(response.content.decode())


def test2():
    with open("C:\\Users\\BaoQiang\\Desktop\\1.txt", 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for item in json_data['emotions']:
            print(item['online_id'])


def main():
    test()


if __name__ == '__main__':
    main()
