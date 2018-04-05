#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : load_data.py
# @Author: JohnHuiWB
# @Date  : 2018/4/3 0003
# @Desc  :
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm


import re
import pandas as pd
from os import path
from csv import reader
from lxml import etree


class LoadData(object):
    def __init__(self):
        self._dir = path.dirname(path.realpath(__file__))
        self._test_data_path = path.join(self._dir, 'test_data.csv')
        self._train_data_path = path.join(self._dir, 'train_data.csv')

    def get_test_data(self):
        return pd.read_csv(self._test_data_path, encoding='utf8')

    def get_train_data(self):
        return pd.read_csv(self._train_data_path, encoding='utf8')


class CreateData(object):
    def __init__(self):
        self._dir = path.dirname(path.realpath(__file__))

    def create_data(self):
        self._create_train_data()
        self._create_test_data()

    def _create_train_data(self):
        data = []
        train_data_path = path.join(self._dir, 'train_data.csv')

        # 根据train.xml生成训练集
        file_path = path.join(self._dir, 'train.xml')
        xml = etree.parse(file_path)  # 解析xml文件
        root = xml.getroot()  # 获取根节点
        e_type_p = {'happiness', 'surprise', 'like'}
        e_type_n = {'fear', 'anger', 'disgust, sadness'}
        # 粒度为sentence，分类为两个list
        for node in root.xpath("//sentence"):
            if node.items()[1][1] == 'Y':
                if node.items()[2][1] in e_type_p:
                    data.append([self._preprocess_weibo_text(node.text), 1])
                elif node.items()[2][1] in e_type_n:
                    data.append([self._preprocess_weibo_text(node.text), 0])

        # 根据train_1.xml生成训练集
        file_path = path.join(self._dir, 'train_1.xml')
        xml = etree.parse(file_path)
        root = xml.getroot()  # 获取根节点
        e_type_p = {'高兴', '喜好', '惊讶'}
        e_type_n = {'愤怒', '恐惧', '悲伤', '厌恶'}
        # 粒度为sentence，分类为两个list
        for node in root.xpath("//sentence"):
            if node.items()[1][1] == 'Y':
                if node.items()[2][1] in e_type_p:
                    data.append([self._preprocess_weibo_text(node.text), 1])
                elif node.items()[2][1] in e_type_n:
                    data.append([self._preprocess_weibo_text(node.text), 0])

        df = pd.DataFrame(data, columns=['text', 'label'])
        df.to_csv(train_data_path, encoding='utf8')

    def _create_test_data(self):
        data = []
        test_data_path = path.join(self._dir, 'test_data.csv')

        with open(path.join(self._dir, 'qzone.csv'), 'r', encoding='utf8') as fp:
            for line in reader(fp):
                data.append(line)

        df = pd.DataFrame(data, columns=['text', 'label'])
        df.to_csv(test_data_path, encoding='utf8')

    @staticmethod
    def _preprocess_weibo_text(text):
        text = re.sub(r'#.*?#', ' ', text)  # 匹配微博的话题
        text = re.sub(r'//@.*?:', ' ', text)  # 匹配微博的用户名
        text = re.sub(r'//@.*?：', ' ', text)  # 匹配微博的用户名（此处冒号为中文冒号）
        return text
