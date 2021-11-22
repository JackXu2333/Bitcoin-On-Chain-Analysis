
# Usage

## Setting Environment

Install Anaconda for virtual python environments. 
Run following command in bash to ensure same working configuration.
```bash
# create new env in Anaconda, python=3.6
conda create -n env_name python=3.6
conda activate env_name
# install pyspark
conda install pyspark=2.3
# install numpy
conda install numpy
# install requests
conda install requests
# install sklearn
conda install -c conda-forge scikit-learn
# install jupyter lab
conda install -c conda-forge jupyterlab=2
# matplotlib
conda install -c conda-forge matplotlib
# install java
conda install -c conda-forge openjdk=8
# check java version
java -version
```

## Fetching Bitcoin Data

Block files store the raw blocks as they were received over the network, which 
are about 128 MB, allocated in 16 MB chunks to prevent excessive fragmentation.

To understand the blockchain raw file structure, we suggest going through the following links:

* [Visualized Block Data](https://www.blockchain.com/btc/block/0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb)
* [Block Data in JSON Format](https://blockchain.info/rawblock/0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb)

Noted they are different representations for the same block with hash: <em>0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb</em>

### Get single raw block data


Wget is useful for downloading a single block raw data, which saves the same block shown 
above into "block706515.blk" file:

```
wget -O block706515.blk "https://blockchain.info/rawblock/0000000000000000000098ff7f0a7841b836064a4e46617e24f51164e626e043?format=hex"
```

### Get multiple raw block data

Please refer to the [get_block_uilts.py](https://git.uwaterloo.ca/c367yang/cs651_final/-/blob/master/src/get_block_uilts.py) for 
detail script function for downloading multiple raw block data file. You can choose to download
either by block heights **blocks_JSON_by_height** or time period **blocks_blk_by_hash** where the blocks are created.

You can also refer to [test_multi_download.py](https://git.uwaterloo.ca/c367yang/cs651_final/-/blob/master/src/test/test_multi_download.py) for 
detail usage of the functions.

### Interpreting raw block data

Noted that 1 BTC = 1e8 satoshi(the smallest unit of Bitcoin)

* [Block Header Doc1](https://developer.bitcoin.org/reference/block_chain.html)
* [Block Header + Transaction Doc2](https://en.bitcoin.it/wiki/Protocol_documentation#tx)



## Constructing Dataset

1. Download raw data into `data` directory. You would see `data/Blocks_612866_610546` directory by default.

```bash
src/test$ python test_multi_download.py
```

2. Transforming raw data into dataset.

see `example_raw_data_process.ipynb` in `src`. You would get `sample.txt` in `data/` .

data format:

 `[time, nBits, value, in_count, out_count]`

* time: Epoch & Unix Timestamp
* value: $10^{-8}$ BTC

