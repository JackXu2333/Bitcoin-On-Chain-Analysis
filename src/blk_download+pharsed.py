#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   blk_download+pharsed.py
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


'''
Download & Phrase raw blk data

Script for combining sequencial operation:
1. download blk raw data
2. phrase blk raw
3. save to disk
'''

if __name__ == "__main__":

    fp = FileParser()
    block = blocks_hashlist_by_time(time.strptime('2020-01-01', '%Y-%m-%d')
                                                      , time.strptime('2020-01-02', '%Y-%m-%d'))
    data_parent_path = "../data/"
    dir = data_parent_path + 'Blocks_' + str(block[0][0]) + '_' + str(
        block[len(block) - 1][0])

    with open(dir + "_parsed.csv", "w") as csv_file:

        print("Begin parsing blocks to %s..." % dir)

        for i in range(len(block)):
            curr = blocks_blk_by_hash(block[1][i], block[0][i])
            fd = FileLoader(curr)
            parsed = fp.parse(fd)

            for j in range(len(parsed)):
                line = ','.join(list(map(str, parsed[j]))) + '\n'
                csv_file.write(line)

            print("%.2f %%, parsing block %d" % ((i + 1) / len(block) * 100, block[0][i]))


