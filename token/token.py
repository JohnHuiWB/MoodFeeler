#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : token.py
# @Author: JohnHuiWB
# @Date  : 2018/4/4 0004
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm

import pickle
from os import path
from keras.preprocessing import sequence
from MoodFeeler.preprocess.ppcr import Seg
from MoodFeeler.data import get_train_data
from keras.preprocessing.text import Tokenizer


class Token(object):
    def __init__(self):
        self._tokenizer = None
        self._s = Seg()
        self._dir = path.dirname(path.realpath(__file__))
        self._tokenizer_path = path.join(self._dir, 'tokenizer.cache')

        if path.exists(self._tokenizer_path):
            print('Load tokenizer.')
            self._load()
        else:
            print('Create and save tokenizer.')
            self._create_tokenizer()
            self._save()

    def _save(self):
        with open(self._tokenizer_path, 'wb') as fp:
            pickle.dump(self._tokenizer, fp)

    def _load(self):
        with open(self._tokenizer_path, 'rb') as fp:
            self._tokenizer = pickle.load(fp)

    def get_tokenizer(self):
        return self._tokenizer

    def _get_processed_data(self, df):
        x = []
        for _, text, label in df.get_values():
            x.append(self._s(text))
        return x

    def _create_tokenizer(self):
        train_data = get_train_data()
        x = self._get_processed_data(train_data)
        # 分词，构建单词-id词典
        self._tokenizer = Tokenizer(split=" ")
        self._tokenizer.fit_on_texts(x)

    def t2s(self, texts, maxlen):
        """
        将每个词用词典中的数值代替
        :return:
        """
        for i in range(len(texts)):
            texts[i] = self._s(texts[i])
        text_ids = self._tokenizer.texts_to_sequences(texts)
        return sequence.pad_sequences(text_ids, maxlen=maxlen)
