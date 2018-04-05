#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'JohnHuiWB'


from MoodFeeler.preprocess.ppcr import Seg


def main():
    s = Seg()
    x = '这里的雨洼刚刚干涸／户外刮起的风带着海水的味道／我只知道那个和这个时候的我很是想念那橙色灯光里跳动的家肴／温暖的被褥／还有临睡前流淌的涓涓细语／其实沉默的环境并不可怕／怕的是沉默的心[泪][泪][泪][泪][泪]'
    print(x)
    print(s(x))


if __name__ == '__main__':
    main()

