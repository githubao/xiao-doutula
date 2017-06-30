#!/usr/bin/env python
# encoding: utf-8

"""
@description: 斗图的关键词搜索爬虫

@author: BaoQiang
@time: 2017/6/30 15:35
"""

import json

import requests
import scrapy
from scrapy.http import FormRequest

from doutula.scrapy.items import Doutu123Item
from doutula.scrapy.settings import FILE_PATH
import re

input_file = '{}/words.txt'.format(FILE_PATH)
out_file = '{}/doutu123.json'.format(FILE_PATH)

headers = {
    'ticket': 'xUSfLshuWc7tmVLqGfynGE'
}

search_fmt = 'http://search.doutu123.com/bbs/?content={}&last_id={}'
topic_fmt = 'http://mobile.doutu123.com/theme/topic/{}'

img_pat = re.compile('http://wxq\.pic\.doutusq\.com/.*?"')


class DoutuMainSpider(scrapy.Spider):
    name = 'doutumain_spider'
    allow_domins = ['doutu123.com']

    def start_requests(self):
        return [FormRequest('http://mobile.doutu123.com/news/', callback=self.parse_search, headers=headers)]

    def parse_search(self, response):
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                attr = line.split('\t')
                if len(attr) != 2:
                    continue

                word, cnt = attr

                yield FormRequest(search_fmt.format(word, 0), callback=self.parse_list, headers=headers,
                                  meta={'word': word})

    def parse_list(self, response):
        word = response.meta['word']

        json_data = json.loads(response.body.decode())

        # 解析数据
        for item in json_data['list']:
            topic_id = item['id']
            yield FormRequest(topic_fmt.format(topic_id), callback=self.parse_item, headers=headers)

        total = json_data['total']
        # 如果有多页，多页请求
        if total % 20 == 0:
            num = total // 20
        else:
            num = total // 20 + 1

        for i in range(1, num):
            yield FormRequest(search_fmt.format(word, num * 20), callback=self.parse_list, headers=headers,
                              meta={'word': word})

    def parse_item(self, response):
        content = response.body.decode()
        json_data = json.loads(content)

        doutu = Doutu123Item()

        doutu['title'] = json_data['post_info']['title']

        url_set = set()
        for item in img_pat.findall(content):
            if '!' in item:
                item = item[:item.find('!')]
                url_set.add(item)

        doutu['urls'] = [url for url in url_set]

        with open(out_file, 'a', encoding='utf-8') as fw:
            fw.write('{}\n'.format(doutu))

            # 最多20个评论就够了，也不要求抓全，懒得写判断条件了...
            # total = json_data['post_info']['comment_num']


def test():
    pat = re.compile('1.')

    s = '12312'

    for i in pat.findall(s):
        print(i)


def main():
    test()


if __name__ == '__main__':
    main()
