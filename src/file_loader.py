#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   file_loader.py
@Time    :   2021/11/07 17:29:19
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   class file loader
'''



class FileLoader:
    offset = 0
    
    def __init__(self, data):
        self.data = data
        
    def read(self, number: int) -> str:
        res = self.data[self.offset: self.offset + number]
        self.offset += number
        return res
    
    def peek(self, number: int) -> str:
        return self.data[self.offset: self.offset + number]