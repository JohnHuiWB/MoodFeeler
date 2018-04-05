#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : test_data.py
# @Author: JohnHuiWB
# @Date  : 2018/4/5 0005
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm


from MoodFeeler.data import get_train_data, get_test_data, create_data


if __name__ == '__main__':
    create_data()
    print(get_test_data)
    print(get_train_data)