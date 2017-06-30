#!/usr/bin/env python
# encoding: utf-8

"""
@description: doutu123 斗图神器 的爬虫

@author: BaoQiang
@time: 2017/6/30 11:02
"""

import scrapy
from scrapy.http import FormRequest
from doutula.scrapy.items import Doutu123Item
from doutula.scrapy.settings import FILE_PATH
import re
import json

out_file = '{}/doutu123.json'.format(FILE_PATH)

url_fmt = 'http://mobile.doutu123.com/news/?last_id={}'


class Doutu123Spider(scrapy.Spider):
    name = 'doutu123_spider'
    allow_domins = ['doutu123.com']

    processed_id = set()

    headers = {
        'ticket': 'xUSfLshuWc7tmVLqGfynGE'
    }

    def start_requests(self):
        return [FormRequest(url_fmt.format(47475973), callback=self.parse_list, headers=self.headers)]

    def parse_list(self, response):
        data = response.body.decode()
        json_data = json.loads(data)

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
            print(json_data)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in res_lst:
                fw.write('{}\n'.format(item))

        if 'last_id' in json_data:
            last_id = json_data['last_id']
            yield FormRequest(url_fmt.format(last_id), callback=self.parse_list, headers=self.headers)


def main():
    print('do sth')


if __name__ == '__main__':
    main()
