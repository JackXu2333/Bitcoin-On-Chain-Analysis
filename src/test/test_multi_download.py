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

from get_block_uilts import *

block_hash, block_height = blocks_hashlist_by_time(time.strptime('2020-01-01', '%Y-%m-%d')
                                                   , time.strptime('2020-01-15', '%Y-%m-%d'))

#assert len(block_hash) == len(block_height)

blocks_blk_by_hash(block_hash, block_height)

#assert os.path.exists("test/Blocks_14_1")
#assert len(os.listdir("test/Blocks_14_1")) == 14
