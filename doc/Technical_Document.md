# CS651 Technical Document
## Model Overview 
* Files are separated into > 5 parts, with train to test ratio being 85:15 or 9:1. Each training set can be not linked in time eg. Train: 1-3, 7-9, 10-12 Test: 4-6
* Testing range: Year **2017 - 2020**
* Model is an aggregate by vote algorithm with k = ..?

* Intake **Comma delimited  .txt** file with each line being the aggregated features from raw BTC and BTC pricing
* Output future price /  current price by hour

## Model Features
::Use BTC-USD as value for BTC::

### Price level features

* last 1 hour / current 
* last 2 hour / current
* last 3 hour / current 
* last 10 hour / current
* last 20 hour / current 
* last 100 hour / current 

### Raw data features

* **Bits** higher the bits, more overall computational power is involved
* **Timestamp** time in ms from 1970.1.1
* **Num of Txnln**
* **Num of TxnOut**
* **Values** in BTC

### Others
* **Halving Schedule** BTC is halved every 4 year (roughly)
* **Minor Identification** If possible
* **Locked Time** Only include when Locked time == 0




