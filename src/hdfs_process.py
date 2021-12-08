#!/usr/bin/python3

from pyspark import SparkConf, SparkContext
import os, sys

class FileLoader:
    offset = 0

    def __init__(self, data):
        self.data = data
        assert (type(self.data) == str)

    def read(self, number):
        res = self.data[self.offset: self.offset + number]
        self.offset += number
        return res

    def peek(self, number):
        return self.data[self.offset: self.offset + number]

class Header:
    def __init__(self, version, p_header_hash, merkle_root_hash, time, nBits, nonce):
        self.version = version
        self.p_header_hash = p_header_hash
        self.merkle_root_hash = merkle_root_hash
        self.time = time
        self.nBits = nBits
        self.nonce = nonce

def convert_endian(s):
    tmp = []
    for i in range(len(s) // 2):
        tmp.insert(0, s[2*i:2*i+2])
    return ''.join(tmp)

def get_header(in_file):
    version = in_file.read(8)
    p_header_hash = in_file.read(64)
    merkle_root_hash = in_file.read(64)
    time = convert_endian(in_file.read(8))
    nBits = convert_endian(in_file.read(8))
    nonce = in_file.read(8)
    return Header(version, p_header_hash, merkle_root_hash, time, nBits, nonce)

def get_compact_size_unit(in_file):
    variable_value = in_file.read(2) # 1B
    if(int(variable_value, 16) < 0xFD):
        value = variable_value # 1B
    else:
        variable_value += in_file.read(2) # 2B
        if(int(variable_value, 16) <= 0xFFFF):
            variable_value += in_file.read(2) # 3B
            value = variable_value[2:] # 2B
        else:
            variable_value += in_file.read(4) # 4B
            if(int(variable_value, 16) <= 0xFFFFFFFF):
                variable_value += in_file.read(2) # 5B
                value = variable_value[2:] # 4B
            else:
                variable_value += in_file.read(10) # 9B
                value = variable_value[2:] # 8B
    return int(convert_endian(value), 16)

class txIn:
    def __init__(self, previous_output, script_length, signature_script, sequence):
        self.previous_output = previous_output
        self.script_length = script_length
        self.signature_script = signature_script
        self.sequence = sequence

def get_tx_in(in_file):
    previous_output = in_file.read(72)
    script_length = get_compact_size_unit(in_file)
    signature_script = in_file.read(script_length*2)
    sequence = in_file.read(8)
    return txIn(previous_output, script_length, signature_script, sequence)

class txOut:
    def __init__(self, value, pk_script_length, pk_script):
        self.value = value
        self.pk_script_length = pk_script_length
        self.pk_script = pk_script

def get_tx_out(in_file):
    value = int(convert_endian(in_file.read(16)), 16)
    pk_script_length = get_compact_size_unit(in_file)
    pk_script = in_file.read(pk_script_length*2)
    return txOut(value, pk_script_length, pk_script)

def read_witness(in_file):
    witness_struct = []
    witness_count = get_compact_size_unit(in_file)
    for _ in range(witness_count):
        witness_len = get_compact_size_unit(in_file)
        witness_struct.append(in_file.read(witness_len * 2))
    return witness_struct

def read_witness_list(in_file, tx_in_count):
    witness_list = []
    for _ in range(tx_in_count):
        witness_list.append(read_witness(in_file))
    return witness_list

class Transaction:
    def __init__(self, version, tx_in_count, tx_in, tx_out_count, tx_out, tx_witness, lock_time):
        self.version = version
        self.tx_in_count = tx_in_count
        self.tx_in = tx_in
        self.tx_out_count = tx_out_count
        self.tx_out = tx_out
        self.tx_witness = tx_witness
        self.lock_time = lock_time

def get_tx(in_file):
    version = convert_endian(in_file.read(8))
    flag = in_file.peek(4)
    if (flag == '0001'):
        in_file.read(4)
    tx_in_count = get_compact_size_unit(in_file)
    tx_in_list = []
    for _ in range(tx_in_count):
        tx_in_list.append(get_tx_in(in_file))
    tx_out_count = get_compact_size_unit(in_file)
    tx_out_list = []
    for _ in range(tx_out_count):
        tx_out_list.append(get_tx_out(in_file))
    if (flag == '0001'):
        tx_witness = read_witness_list(in_file, tx_in_count)
    else:
        tx_witness = []
    lock_time = convert_endian(in_file.read(8))
    return Transaction(version, tx_in_count, tx_in_list,
                       tx_out_count, tx_out_list, tx_witness, lock_time)

class FileParser:
    def parse(self, fl):
        header = get_header(fl)
        txn_count = get_compact_size_unit(fl)
        output = []
        for _ in range(txn_count):
            tx = get_tx(fl)
            tx_out_list = tx.tx_out

            value = 0
            for tx_out in tx_out_list:
                value += tx_out.value

            output.append([int(header.time,16), int(header.nBits, 16), value, tx.tx_in_count, tx.tx_out_count])
        return output

def toCSVLine(data):
    return ','.join(str(d) for d in data)

def runSpark(fpath, opath):
    conf = SparkConf().setAppName("BTC_2018")
    conf = (conf.set('spark.executor.memory', '24G')
            .set('spark.driver.memory', '8G')
            .set('spark.driver.maxResultSize', '10G'))
    sc = SparkContext(conf=conf)

    fp = FileParser()

    # [time, nBits, value, in_count, in_min, in_max, out_count, out_min, out_max, count]
    raw_data = sc.textFile(fpath, 10)

    test = raw_data.flatMap(lambda blk:
                            fp.parse(FileLoader(blk)))
    test = test.map(lambda x: (x[0] // 3600, (x[1], x[2], x[3], x[4], 1,
                                              x[2], x[2], x[3], x[3], x[4], x[4])))



    test = test.reduceByKey(lambda a, b: (
        a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3], a[4] + b[4],
        min(a[5], b[5]), max(a[6], b[6]), min(a[7], b[7]), max(a[8], b[8]),
        min(a[9], b[9]), max(a[10], b[10])))
    test = test.map(lambda x: str(x[0]) + ',' + toCSVLine(x[1]))
    test.saveAsTextFile(opath)

if __name__ == "__main__":

    os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"

    try:
        if len(sys.argv) < 3:
            print("usage: " + sys.argv[0] + " [inpath] [outpath]")
            exit(1)

        runSpark(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)
