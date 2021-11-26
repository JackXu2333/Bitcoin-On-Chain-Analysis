#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_decoder_485300.py
@Time    :   2021/11/07 17:29:01
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   test code
'''

import sys

sys.path.append('..')

from file_loader import FileLoader
from transaction import *
from utils import *
from header import *

with open('../../data/block485300.blk', 'r') as in_file:
    fd = FileLoader(in_file.readline())
    header = get_header(fd)
    assert int(header.time,
               16) == 1505436186  # must be 1505436186 for the block 485300
    print(int(header.time, 16))
    txn_count = get_compact_size_unit(fd)
    tx = get_tx(fd)
    print(tx.tx_in_count)
    print(tx.tx_out_count)
