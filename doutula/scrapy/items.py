# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import json


class DoutulaItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)

class UBiaoQingItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)