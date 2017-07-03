#!/usr/bin/env python
# encoding: utf-8

"""
@description: 六只脚数据爬虫

@author: BaoQiang
@time: 2017/7/3 10:53
"""

import random
import time
import json

import scrapy
from scrapy import Request

from doutula.pth import FILE_PATH
from doutula.scrapy.items import SixFootItem

out_file = '{}/sixfoot.json'.format(FILE_PATH)

root_url = 'http://foooooot.com'

search_url_fmt = 'http://foooooot.com/client2/search/trip/?keyword=&limit=100&recommend=recommend&start_timestamp={}'


class SixFootSpider(scrapy.Spider):
    name = 'sixfoot_spider'
    allow_domins = ['foooooot.com']

    def start_requests(self):
        return [Request(search_url_fmt.format(0), callback=self.parse_item)]

    def parse_item(self, response):
        json_data = json.loads(response.body.decode())

        res_list = []
        for item in json_data['data']:
            if item['pic_footprint_count'] >= 100:
                six = SixFootItem()
                six['id'] = item['id']
                six['name'] = item['name']
                six['activity'] = item['activity']
                six['voteup'] = item['pic_footprint_count']

                res_list.append(six)

            next_ts = item['create_time']

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in res_list:
                fw.write('{}\n'.format(item))

        yield Request(search_url_fmt.format(next_ts), callback=self.parse_item)


def main():
    print(random.random())
    print(time.time())


if __name__ == '__main__':
    main()
