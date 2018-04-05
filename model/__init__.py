#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : __init__.py.py
# @Author: JohnHuiWB
# @Date  : 2018/4/5 0005
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm

from MoodFeeler.model.model import Model

m = Model()
eval = m.eval
predict = m.predict
train = m.train
draw_model = m.draw_model