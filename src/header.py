#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   header.py
@Time    :   2021/11/07 17:29:37
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   decode header for the raw data
'''


from file_loader import FileLoader
from utils import *
# protocol header of bitcoin

class Header:
    def __init__(self, version, p_header_hash, merkle_root_hash, time, nBits, nonce):
        self.version = version
        self.p_header_hash = p_header_hash
        self.merkle_root_hash = merkle_root_hash
        self.time = time
        self.nBits = nBits
        self.nonce = nonce
        
        
'''
input: file_loader
output: class Header
'''
def get_header(in_file: FileLoader) -> Header:
    version = in_file.read(8)
#     print('version =', version)
    p_header_hash = in_file.read(64)
#     print(p_header_hash)
    merkle_root_hash = in_file.read(64)
#     print(merkle_root_hash)
    time = convert_endian(in_file.read(8))
#     print('time = ', time)
    nBits = convert_endian(in_file.read(8))
#     print('nBits = ', nBits)
    nonce = in_file.read(8)
#     print('nonce = ', nonce)
    return Header(version, p_header_hash, merkle_root_hash, time, nBits, nonce)