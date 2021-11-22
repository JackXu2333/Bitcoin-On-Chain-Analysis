#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   file_parse.py
@Time    :   2021/11/20 16:11:26
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   file parse class
'''

from file_loader import FileLoader
from transaction import *
from utils import *
from header import *

class FileParser:
    # get [create time, nBits, value, in_count, out_count]
    def parse(self, fl: FileLoader):
        header = get_header(fl)
        txn_count = get_compact_size_unit(fl)
        output = []
        for _ in range(txn_count):
            tx = get_tx(fl)
            # class tx out: [value, pk_script_length, pk_script]
            tx_out_list = tx.tx_out

            value = 0
            for tx_out in tx_out_list:
                value += tx_out.value

            output.append([int(header.time,16), int(header.nBits, 16), value, tx.tx_in_count, tx.tx_out_count])
        return output