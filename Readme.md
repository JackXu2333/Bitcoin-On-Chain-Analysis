

# Setting Environment

```bash
# create new env in Anaconda, python=3.6
conda create -n env_name python=3.6
conda activate env_name
# install pyspark
conda install pyspark=2.3
# install numpy
conda install numpy
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





# Processing Data

## get block hex raw data

Block files store the raw blocks as they were received over the network.

Block files are about 128 MB, allocated in 16 MB chunks to prevent excessive fragmentation.

Here, we can have a look at the

[visualized block data](https://www.blockchain.com/btc/block/0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb)

[block data in json format](https://blockchain.info/rawblock/0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb)

use wget download the block raw data

```
wget -O block706515.blk "https://blockchain.info/rawblock/0000000000000000000304ad8a7cb419a8889c09a74317df07b681e2d3d1a7fb?format=hex"
```

## interpret raw data

1 BTC = 1e8 satoshi(the smallest unit of Bitcoin)



[Block Header Doc1](https://developer.bitcoin.org/reference/block_chain.html)

[Block Header + Transaction Doc2](https://en.bitcoin.it/wiki/Protocol_documentation#tx)



