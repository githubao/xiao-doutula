#!/usr/bin/env python
# encoding: utf-8

"""
@description: 六只脚数据爬虫

@author: BaoQiang
@time: 2017/7/3 10:53
"""

import json
import time

import requests
import scrapy
from scrapy import Request
from xml.etree import ElementTree as et
import traceback

from doutula.pth import FILE_PATH
from doutula.scrapy.items import SixFootItem

out_file = '{}/sixfoot.json'.format(FILE_PATH)
out_file2 = '{}/sixfoot_new.json'.format(FILE_PATH)

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
            if item['pic_footprint_count'] >= 0:
                six = SixFootItem()
                six['id'] = item['id']
                six['name'] = item['name']
                six['activity'] = item['activity']
                six['voteup'] = item['pic_footprint_count']
                six['latitude'] = item['latitude']
                six['lngitude'] = item['lngitude']

                res_list.append(six)

            next_ts = item['create_time']

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in res_list:
                fw.write('{}\n'.format(item))

        yield Request(search_url_fmt.format(next_ts), callback=self.parse_item)


def run():
    google_apis_fmt = 'http://maps.google.com/maps/api/geocode/xml?latlng={:0.6f},{:0.6f}&language=zh-CN&sensor=false'

    with open(out_file, 'r', encoding='utf-8') as f, \
            open(out_file2, 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()

            json_data = json.loads(line)
            try:
                url = google_apis_fmt.format(json_data['latitude'], json_data['lngitude'])
                response = requests.get(url, proxies={
                    'http': 'http:127.0.0.1:8123',
                    'https': 'http:127.0.0.1:8123'
                })
                json_data['loc'] = parse_res(response)
            except Exception as e:
                traceback.print_exc()

            json.dump(json_data, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')

            # break


def parse_res(res):
    doc = et.fromstring(res.content.decode())
    return doc.find('result')[1].text


def test():
    # print(random.random())
    # print(time.time())

    # 2010 - 03 - 03 14: 38:24
    # st = time.localtime(1267598304)
    # print(time.strftime('%Y-%m-%d %H:%M:%S', st))

    fmt = '{:0.6f}'
    print(fmt.format(0.535))


def run2():
    with open('C:\\Users\\BaoQiang\\Desktop\\sixfoot_new.json', 'r', encoding='utf-8') as f, \
            open('C:\\Users\\BaoQiang\\Desktop\\sixfoot.json', 'w', encoding='utf-8') as fw:
        res_list = []
        for line in f:
            res_list.append(json.loads(line.strip()))

        sorted_list = sorted(res_list, key=lambda x: x['voteup'], reverse=True)

        for item in sorted_list:
            json.dump(item, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def main():
    # test()
    # run()
    run2()


if __name__ == '__main__':
    main()
