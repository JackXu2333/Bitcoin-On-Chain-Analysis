#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   transaction.py
@Time    :   2021/11/07 17:29:58
@Author  :   Chengzhang Yang
@Version :   1.0
@Contact :   c367yang@uwaterloo.ca
@Desc    :   decode the transaction part for the raw data
'''



from utils import *
from file_loader import FileLoader

# protocol documentation: https://en.bitcoin.it/wiki/Protocol_documentation#tx

# ============= transaction in ========================

class txIn:
    def __init__(self, previous_output, script_length, signature_script, sequence):
        self.previous_output = previous_output
        self.script_length = script_length
        self.signature_script = signature_script
        self.sequence = sequence

'''
input: file_loader
output: class txIn
'''
def get_tx_in(in_file: FileLoader) -> txIn:
    previous_output = in_file.read(72)
    # print("previous output = ", previous_output)
    script_length = get_compact_size_unit(in_file)
    # print("script_length = ", script_length)
    signature_script = in_file.read(script_length*2)
#     print("signature_script = ", signature_script)
    sequence = in_file.read(8)
#     print("sequence = ", sequence)
    return txIn(previous_output, script_length, signature_script, sequence)

# ============= transaction out ========================


class txOut:
    def __init__(self, value, pk_script_length, pk_script):
        self.value = value
        self.pk_script_length = pk_script_length
        self.pk_script = pk_script

'''
input: file_loader
output: class txOut
'''
def get_tx_out(in_file: FileLoader) -> txOut:
    value = int(convert_endian(in_file.read(16)), 16)
    # print("value = ", value)
    pk_script_length = get_compact_size_unit(in_file)
    # print("pk_script_length = ", pk_script_length)
    pk_script = in_file.read(pk_script_length*2)
    # print("pk_script = ", pk_script)
    return txOut(value, pk_script_length, pk_script)


# ============= transaction witness ========================

'''
input: file_loader, witness_count
output: list of witness
'''
def read_witness_list(in_file: FileLoader, tx_in_count: int):
    witness_list = []
    for _ in range(tx_in_count):
        witness_list.append(read_witness(in_file))
    return witness_list

'''
input: file_loader
output: class tx_witness
The TxWitness structure consists of a var_int count of witness data components, 
followed by (for each witness data component) a var_int length of the component and the raw component data itself.
'''
def read_witness(in_file: FileLoader):
    witness_struct = []
    witness_count = get_compact_size_unit(in_file)
    for _ in range(witness_count):
        witness_len = get_compact_size_unit(in_file)
        witness_struct.append(in_file.read(witness_len * 2))
    return witness_struct

# ============= transaction = ========================

class Transaction:
    def __init__(self, version, tx_in_count, tx_in, tx_out_count, tx_out, tx_witness, lock_time):
        self.version = version
        self.tx_in_count = tx_in_count
        self.tx_in = tx_in
        self.tx_out_count = tx_out_count
        self.tx_out = tx_out
        self.tx_witness = tx_witness
        self.lock_time = lock_time


'''
input: file_loader
output: class Transaction
'''
def get_tx(in_file: FileLoader) -> Transaction:
    version = convert_endian(in_file.read(8))
#     print('version =', version)
    
    # optional variable, always 0001
    flag = in_file.peek(4) # If present, always 0001
    # print('flag = ', flag)

    if(flag == '0001'):
        in_file.read(4)
    
    tx_in_count = get_compact_size_unit(in_file)
    # print('tx_in count = ', tx_in_count)
    
    tx_in_list = []
    for _ in range(tx_in_count):
        tx_in_list.append(get_tx_in(in_file))
    
    tx_out_count = get_compact_size_unit(in_file)
    # print('tx_out count', tx_out_count)
    
    tx_out_list = []
    for _ in range(tx_out_count):
        tx_out_list.append(get_tx_out(in_file))

    # ignore stupid tx_witness and lock time
    # but of course we still need to read it 
    if(flag == '0001'):
        tx_witness = read_witness_list(in_file, tx_in_count)
    else:
        tx_witness = []
        
    lock_time = convert_endian(in_file.read(8))
    return Transaction(version, tx_in_count, tx_in_list, \
                       tx_out_count, tx_out_list, tx_witness, lock_time)
        
