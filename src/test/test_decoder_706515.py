#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_decoder_706515.py
@Time    :   2021/11/07 17:28:38
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   test code
'''

from file_loader import FileLoader
from transaction import *
from utils import *
from header import *

with open('./data/block706515.blk', 'r') as in_file:
    fd = FileLoader(in_file.readline())
    header = get_header(fd)
    print(int(header.time, 16))
    assert int(header.time, 16) == 1635113163

    txn_count = get_compact_size_unit(fd)

    print('txn count = ', txn_count)
    assert txn_count == 553

    print('=========transaction=============')
    total_in = 0
    total_out = 0
    for _ in range(txn_count):
        tx = get_tx(fd)
        total_in += tx.tx_in_count
        total_out += tx.tx_out_count
    print('total in = ', total_in, "total out", total_out)

    assert total_in == 3615
    assert total_out == 1544
