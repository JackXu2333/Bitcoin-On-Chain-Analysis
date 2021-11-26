#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_block_utils.py
@Time    :   2021/11/07 17:30:19
@Author  :   Sijie Xu (jack)
@Version :   0.1
@Contact :   s362xu@uwaterloo.ca
@Desc    :   utils for block pulling
'''


import os
import json
import calendar
import time
import requests


'''
store blocks locally in blk format
input:
    block_hash: list of block hashes
    block_height: list of block heights with respect to hashes
output: dir of files labelled block_${height}.blk
'''

def multiblocks_blk_by_hash (block = [], file_format = True, data_parent_path = "../../data/"):

    if len(block) == 0:
        print("Empty blk hash list")
        return -1

    # Make dir
    dir = data_parent_path + 'Blocks_' + str(block[0][0]) + '_' + str(block[len(block) - 1][0])
    if not os.path.exists(dir) and file_format:
        os.makedirs(dir)

    print("Begin hashing blocks to %s..." % dir)

    for count, value in enumerate(block):
        print("%.2f %%, hashing block %d" % ((count+1) / len(block) * 100, value[0]))
        blocks_blk_by_hash(value[1], value[0], True, dir)

    return 0

def blocks_blk_by_hash(block_hash: str, block_height: int, file_format = False, dir = ""):

    url = 'https://blockchain.info/rawblock/' + block_hash + '?format=hex'
    data = requests.get(url).text

    if file_format:
        with open(dir + "/block_" + str(block_height) +".blk", "w") as blk_file:
            blk_file.write(data)
    else:
        return data

    return 0


'''
return hash list from given period
WARNING: default settings is every hash on record
input:
    start date: default = 2009-01-03 (data of BTC online)
    end date: default = current data
output: 
    List of block hashes
    List of block heights with respect to block hashes
'''


def blocks_hashlist_by_time(start_date=time.strptime('2009-01-10', '%Y-%m-%d')
                       , end_date=time.gmtime()):

    # Convert dates
    start_date_epoch = calendar.timegm(start_date)
    end_date_epoch = calendar.timegm(end_date)
    start_date_str = time.strftime("%Y-%m-%d", start_date)
    end_date_str = time.strftime("%Y-%m-%d", end_date)

    if end_date_epoch < start_date_epoch:
        print("Start date must > end date")
        return -1

    # Record hash list in list
    block = []

    for i in range(start_date_epoch, end_date_epoch + 1, 86400):
        url = 'https://blockchain.info/blocks/' + str(i) + '000?format=json'
        #print(url)
        data = requests.get(url).json()

        if len(data) == 0:
            end_date_str = time.strftime("%Y-%m-%d", time.gmtime(i))
            break

        current_block = []

        for p in data:
            current_block.append((p['block_index'], p['hash']))

        block = current_block + block

    # Print start end date
    print("Start: " + start_date_str + " End: " + end_date_str)
    return block

'''
store blocks locally in JSON format
!!currently incompatible with blk workflow!!
input:
    block height start: default = 0 (beginning block)
    block height end
output: json block files in directory Blocks_start_end
'''


def blocks_JSON_by_height(block_height_start=0, block_height_end=1):
    # Handle input error
    if block_height_start < 0 or block_height_end < 0:
        print("Invalid block height")
        return -1
    elif block_height_start > block_height_end:
        print("Start should <= end")
        return -1

    # Make dir
    dir = 'Blocks_' + str(block_height_start) + '_' + str(block_height_end)
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i in range(block_height_start, block_height_end + 1):
        url = 'https://blockchain.info/block-height/' + str(i) + '?format=json'
        data = requests.get(url).json()

        # Write to dir
        with open(dir + '/block_' + str(i) + '.json', 'w') as outfile:
            json.dump(data, outfile)

        if len(data['blocks']) == 0:
            block_height_end = i
            break

    print(
        "Start: " + str(block_height_start) + " End: " + str(block_height_end))
    return 0
