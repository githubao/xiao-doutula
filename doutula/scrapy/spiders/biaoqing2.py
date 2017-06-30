#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: BaoQiang
@time: 2017/6/22 11:04
"""

import scrapy
from scrapy import Request
from doutula.scrapy.items import UBiaoQingItem
from doutula.pth import FILE_PATH
import traceback
import re

url_pat = re.compile('http://www.ubiaoqing.com/biaoqingbao/([\d]+)')

input_file = '{}/words.txt'.format(FILE_PATH)
out_file = '{}/biaoqing_item.json'.format(FILE_PATH)

root_url = 'http://www.ubiaoqing.com/'


class UBiaoQingSpider(scrapy.Spider):
    name = 'ubiaoqing2_spider'
    allow_domins = ['ubiaoqing.com']

    processed_id = set()

    def start_requests(self):
        return [Request('http://www.ubiaoqing.com', callback=self.parse_list)]

    def parse_list(self, response):
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                attr = line.split('\t')
                if len(attr) != 2:
                    print('err line: {}'.format(line))
                    continue
                word, cnt = attr

                yield Request(search_url_fmt.format(word), callback=self.parse_item)

    def parse_item(self, response):
        biaoqing_list = []

        try:
            li_lst = response.selector.xpath('//div[contains(@class,"center-block")]//li//a')

            for item in li_lst:
                biaoqing = UBiaoQingItem()
                biaoqing['url'] = item.xpath('./@href')[0].extract().strip().replace('../', root_url)

                bid = get_id(biaoqing['url'])
                if not bid:
                    continue

                biaoqing['src_url'] = item.xpath('./img/@src')[0].extract().strip()
                tags_lst = item.xpath('./img/@alt')[0].extract().strip().split()
                biaoqing['tags'] = [item.strip('表情包') for item in tags_lst]

                if not bid in self.processed_id:
                    self.processed_id.add(bid)
                    biaoqing['id'] = bid
                    biaoqing_list.append(biaoqing)

        except Exception as e:
            traceback.print_exc()
            print(response)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in biaoqing_list:
                fw.write('{}\n'.format(item))


search_url_fmt = 'http://www.ubiaoqing.com/search/{}'


def get_id(url):
    m = url_pat.match(url)
    if m:
        return m.group(1)


def main():
    pass


if __name__ == '__main__':
    main()
