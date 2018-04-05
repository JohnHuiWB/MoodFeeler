#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'JohnHuiWB'


import re
import os
import jieba
from zhon.hanzi import punctuation
from zhon.pinyin import non_stops, stops


class Seg(object):
    """
    载入数据，分词，去停用词
    """

    def __init__(self, file_path_of_stopwords='all_stopword.txt'):
        jieba.initialize()  # 初始化jieba

        self._file_path_of_stopwords = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            file_path_of_stopwords)

    def __call__(self, text: str):
        """
        传入一个文本文件的内容，完成预处理、分词和去停用词
        返回生成的文本，每个词之间用空格分隔
        """
        text_treated = self._pretreat(text)  # 文本预处理
        seg_list = self._jieba_seg(text_treated)  # jieba分词
        result = self._stop_word(seg_list)  # 去停用词

        return result

    @staticmethod
    def _jieba_seg(text_treated):
        """
        传入预处理完成的文本
        jieba分词
        返回分词完成的list
        """
        if not os.path.exists('dict.txt'):
            pass
        else:
            # 如果当期目录下存放有自定义的词典，则导入该词典
            jieba.load_userdict('dict.txt')

        return jieba.cut(text_treated, cut_all=False)

    @staticmethod
    def _pretreat(text):
        """
        传入文本
        处理文本中无关的符号
        返回处理完毕的文本
        """
        text = re.sub(r'[A-Za-z\\]+', '', text)
        r = r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
        text = re.sub(r"[%s+]" % punctuation, '', text)
        text = re.sub(r"[%s+]" % non_stops, '', text)
        text = re.sub(r"[%s+]" % stops, '', text)
        text = re.sub(r, '', text)
        text = text.strip()
        text = re.sub(r"\d{5,6000}", '', text)

        return text

    def _stop_word(self, seg_list):
        """
        传入seg_list
        去停用词
        返回结果
        """
        stopwords = self._get_stopwords()

        li = []
        for word in seg_list:
            if word not in stopwords:
                if word != '\t':
                    li.append(word)
        result = str(' '.join(li))

        return result

    def _get_stopwords(self):
        """
        获取停用词
        """
        if not os.path.exists(self._file_path_of_stopwords):
            print('停用词文件不存在!!!')
            exit(1)

        with open(self._file_path_of_stopwords, 'rb') as fp:
            stopwords_set = {line.strip().decode('utf-8') for line in fp}

        return stopwords_set
