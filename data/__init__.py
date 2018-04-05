#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : __init__.py
# @Author: JohnHuiWB
# @Date  : 2018/4/3 0003
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm

from MoodFeeler.data.load_data import LoadData, CreateData

l = LoadData()
get_train_data = l.get_train_data
get_test_data = l.get_test_data
c = CreateData()
create_data = c.create_data