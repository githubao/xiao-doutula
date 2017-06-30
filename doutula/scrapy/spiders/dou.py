#!/usr/bin/env python
# encoding: utf-8

"""
@description: 斗图爬虫

@author: BaoQiang
@time: 2017/5/16 12:34
"""

import scrapy
from scrapy import Request
from doutula.scrapy.items import DoutulaItem
from doutula.pth import FILE_PATH

output_path = '{}/doutu_item.json'.format(FILE_PATH)


class DoutulaSpider(scrapy.Spider):
    name = 'doutula_spider'
    allow_domins = ['doutula.com']

    def start_requests(self):
        return [Request('https://www.doutula.com', callback=self.parse_page)]

    def parse_page(self, response):
        # for i in range(1, 820):
        for i in range(1, 2):
            yield Request(list_url.format(i), callback=self.parse_list)

    def parse_list(self, response):
        classes = response.selector.xpath('//div[@class="page-content"]/a')

        result_list = []
        for item in classes:
            doutu = DoutulaItem()

            doutu['url'] = item.xpath('./@href')[0].extract().strip()
            doutu['title'] = ''.join([i.extract().strip() for i in item.xpath('.//text()')])
            # doutu['src'] = item.xpath('./img[contains(@class,"img-responsive")]/@src')[0].extract().strip()
            doutu['src_ori'] = item.xpath('./img[contains(@class,"img-responsive")]/@data-original')[
                0].extract().strip().strip('//|!dta')
            doutu['src_bak'] = item.xpath('./img[contains(@class,"img-responsive")]/@data-backup')[
                0].extract().strip().strip('//|!dta')

            result_list.append(doutu)

        with open(output_path, 'a', encoding='utf-8') as fw:
            for item in result_list:
                fw.write('{}\n'.format(item))


list_url = 'https://www.doutula.com/photo/list/?page={}'


def main():
    print('do sth')


if __name__ == '__main__':
    main()
