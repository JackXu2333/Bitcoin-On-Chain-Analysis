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

if __name__ == "__main__":

    fp = FileParser()
    block_hash, block_height = blocks_hashlist_by_time(time.strptime('2020-01-01', '%Y-%m-%d')
                                                      , time.strptime('2020-01-02', '%Y-%m-%d'))
    data_parent_path = "../../data/"
    dir = data_parent_path + 'Blocks_' + str(block_height[0]) + '_' + str(
        block_height[len(block_height) - 1])

    with open(dir + "_parsed.csv", "w") as csv_file:

        print("Begin parsing blocks to %s..." % dir)

        for i in range(len(block_hash)):
            curr = blocks_blk_by_hash(block_hash[i], block_height[i])
            fd = FileLoader(curr)
            parsed = fp.parse(fd)

            for j in range(len(parsed)):
                line = ','.join(list(map(str, parsed[j]))) + '\n'
                csv_file.write(line)

            print("%.2f %%, parsing block %d" % ((i + 1) / len(block_hash) * 100, block_height[i]))

# multiblocks_blk_by_hash(block_hash, block_height)

