# Interpret Raw Data

## Raw Block data (blk*.dat)

Block files store the raw blocks as they were received over the network.

Block files are about 128 MB, allocated in 16 MB chunks to prevent excessive fragmentation.

```
https://blockchain.info/rawblock/00000000000000000003c1f0ea7a6786de8225ab55e6413c67df1446c398f5a7
```

### 下载block

```
wget -O block708253.blk "https://blockchain.info/rawblock/00000000000000000003c1f0ea7a6786de8225ab55e6413c67df1446c398f5a7?format=hex"
```

```
wget -O block708253.blk "https://blockchain.info/rawblock/00000000000000000003c1f0ea7a6786de8225ab55e6413c67df1446c398f5a7?format=hex"
```



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

