#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Ssfanli
@Time  : 2020/04/14 10:39 下午
@Desc  : demo
"""

from screcord import record
import time


@record(
    platform='android',             # 'a', 'android'
    device='TEV0217315000851',      # android device id or iOS udid
    file_path='./demo1.mp4',        # mp4 file path
    offset=(1, 1),                  # default (1, 1), mean of: before record sleep 1s and after record sleep 1s
    pre_kill=True                   # default True, before start whether kill or not
)
def android_case(t: int):
    for i in range(t):
        time.sleep(1)
        print(t - i)


@record(
    platform='ios',                         # 'i', 'ios'
    device='00008020-001D1D900CB9002E',     # iOS UDID
    file_path='./demo2.mp4',                # video file path
    offset=(2, 1),                          # same as android
    pre_kill=True,                          # same as android
                                            # Refs: https://github.com/WPO-Foundation/xrecord
)
def ios_case(t: int):
    for i in range(t):
        time.sleep(1)
        print(t - i)


if __name__ == '__main__':

    android_case(3)
    ios_case(5)





