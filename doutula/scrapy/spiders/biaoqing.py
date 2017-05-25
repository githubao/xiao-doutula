#!/usr/bin/env python
# encoding: utf-8

"""
@description: 表情包

@author: BaoQiang
@time: 2017/5/25 14:21
"""

import scrapy
from scrapy import Request
from doutula.scrapy.items import UBiaoQingItem
from doutula.scrapy.settings import FILE_PATH

output_path = '{}/biaoqing_item.json'.format(FILE_PATH)


class UBiaoQingSpider(scrapy.Spider):
    name = 'ubiaoqing_spider'
    allow_domins = ['ubiaoqing.com']

    def start_requests(self):
        return [Request('http://www.ubiaoqing.com', callback=self.parse_list)]

    def parse_list(self, response):
        # for i in range(1, 360000):
        for i in range(1, 11):
            yield Request(item_url_fmt.format(i), callback=self.parse_item, meta={'id': i})

    def parse_item(self, response):
        biaoqing = UBiaoQingItem()

        biaoqing['url'] = response.url
        biaoqing['id'] = response.meta['id']

        img_url = response.selector.xpath('//div[contains(@class,"panel-body")]/div/img')
        biaoqing['src_url'] = img_url.xpath('@src')[0].extract().strip()
        # biaoqing['title'] = img_url.xpath('@title')[0].extract().strip()

        tags_url = response.selector.xpath('//ul[contains(@class,"tag-list")]//strong/text()')
        biaoqing['tags'] = [item.extract().strip() for item in tags_url]

        with open(output_path, 'a', encoding='utf-8') as fw:
            fw.write('{}\n'.format(biaoqing))


item_url_fmt = 'http://www.ubiaoqing.com/biaoqingbao/{}'


def main():
    print('ecff53dddd655de1fdd321b57408db28'.__len__())


if __name__ == '__main__':
    main()
