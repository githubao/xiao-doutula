#!/usr/bin/env python
# encoding: utf-8

"""
@description: 排序数据

@author: BaoQiang
@time: 2017/6/30 17:04
"""

from doutula.pth import FILE_PATH
import jieba
import re
import math
from collections import defaultdict
import random

word_file = '{}/words.txt'.format(FILE_PATH)

hanzi_pat = re.compile('[\u4e00-\u9fff]')

max_num = 10
ran_num = 5

datas = [
    {'word': '我', 'img_urls': [1, 3, 4]},
    {'word': '我', 'img_urls': [1, 3, 5]},
    {'word': '喜欢', 'img_urls': [2, 4, 5]},
    {'word': '你', 'img_urls': [1, 3, 5]},
]

# total_cnt = 242044180
total_cnt = 1000000
default_cnt = 10000

word_dic = {}


def run(query):
    query = trim_data(query)

    word_lst = jieba.cut(query)

    weight_dic = cal_weight(word_lst)

    if not weight_dic:
        return

    img_score = cal_score(weight_dic)

    sorted_img = sorted(img_score.items(), key=lambda x: x[1], reverse=True)

    if len(sorted_img) > max_num:
        sorted_img = sorted_img[:max_num]

    return random.sample(sorted_img, ran_num) if len(sorted_img) > ran_num else sorted_img


def cal_score(weight_dic):
    dic = defaultdict(float)

    keys = weight_dic.keys()

    for item in datas:
        word = item['word']
        if word in keys:
            imgs = item['img_urls']

            for url in imgs:
                dic[url] += weight_dic[word]

    return dic


def cal_weight(word_lst):
    global word_dic
    if not word_dic:
        word_dic = load_words()

    word_cnt = {word: word_dic.get(word, default_cnt) for word in word_lst}
    word_log = {word: -math.log10(cnt / total_cnt) for word, cnt in word_cnt.items()}
    total_weight = sum(word_log.values())

    if total_weight == 0:
        return

    word_weight = {word: weight / total_weight for word, weight in word_log.items()}
    return word_weight


def trim_data(line):
    new_line = ''.join(i for i in hanzi_pat.findall(line))

    # TODO 去除停止词

    return new_line


def load_words():
    res_dic = {}
    with open(word_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            attr = line.split('\t')

            res_dic[attr[0]] = int(attr[1])

    return res_dic


def main():
    s = '我喜欢。你'
    print(run(s))


if __name__ == '__main__':
    main()
