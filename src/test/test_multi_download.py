#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_multi_download.py
@Time    :   2021/11/08 17:28:38
@Author  :   Sijie Xu (Jack)
@Version :   1.0
@Contact :   s362xu@uwaterloo.ca
@Desc    :   test code
'''
import sys
sys.path.append('..')

from get_block_uilts import *
from file_parse import *

block = blocks_hashlist_by_time(time.strptime('2020-01-01', '%Y-%m-%d')
                                                      , time.strptime('2020-01-02', '%Y-%m-%d'))
multiblocks_blk_by_hash(block)

