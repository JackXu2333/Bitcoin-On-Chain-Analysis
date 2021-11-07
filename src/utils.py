#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2021/11/07 17:30:19
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   utils module
'''



'''
endian conversion
big endian -> little endian 
little endian -> big endian

input: string
output: string
''' 
from file_loader import FileLoader


def convert_endian(s: str) -> str:
    tmp = []
    for i in range(len(s) // 2):
        tmp.insert(0, s[2*i:2*i+2])
    return ''.join(tmp)


'''
get a compact variable from the file loader
input: file_loader
output: int compact_variable
'''
def get_compact_size_unit(in_file: FileLoader) -> int:
    variable_value = in_file.read(2) # 1B
#     print("variable = ", variable_value)
    # storage length == 1
    # longer numbers are encoded in little endian
    if(int(variable_value, 16) < 0xFD):
        value = variable_value # 1B
    else:
        variable_value += in_file.read(2) # 2B 
        # storage length == 3
        if(int(variable_value, 16) <= 0xFFFF):
            variable_value += in_file.read(2) # 3B
            value = variable_value[2:] # 2B
        else:
            variable_value += in_file.read(4) # 4B
            # storage length == 5
            if(int(variable_value, 16) <= 0xFFFFFFFF):
                variable_value += in_file.read(2) # 5B
                value = variable_value[2:] # 4B
            # storage length == 9
            else:
                variable_value += in_file.read(10) # 9B
                value = variable_value[2:] # 8B
    return int(convert_endian(value), 16)