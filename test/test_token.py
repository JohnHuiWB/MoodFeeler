#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : test_token.py
# @Author: JohnHuiWB
# @Date  : 2018/4/5 0005
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm

from MoodFeeler.token import get_tokenizer, t2s

if __name__ == '__main__':
    tokenizer = get_tokenizer()
    # print(tokenizer.word_index)

    s = '命运如同手中的掌纹，无论多曲折，始终掌握在自己手中...'
    vec = t2s([s], 40)
    print(vec)