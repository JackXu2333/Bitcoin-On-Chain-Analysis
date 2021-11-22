## Block

The **block** message is sent in response to a getdata message which requests transaction information from a block hash.

| Field Size | Description |                          Data type                           |                           Comments                           |
| :--------: | :---------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     4      |   version   |                           int32_t                            |       Block version information (note, this is signed)       |
|     32     | prev_block  |                           char[32]                           | The hash value of the previous block this particular block references |
|     32     | merkle_root |                           char[32]                           | The reference to a Merkle tree collection which is a hash of all transactions related to this block |
|     4      |  timestamp  |                           uint32_t                           | A Unix timestamp recording when this block was created (Currently limited to dates before the year 2106!) |
|     4      |    bits     |                           uint32_t                           | The calculated [difficulty target](https://en.bitcoin.it/wiki/Difficulty) being used for this block |
|     4      |    nonce    |                           uint32_t                           | The nonce used to generate this block… to allow variations of the header and compute different hashes |
|     1+     |  txn_count  | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |                Number of transaction entries                 |
|     ?      |    txns     |                             tx[]                             |        Block transactions, in format of "tx" command         |





## Block Headers

| Field Size | Description |                          Data type                           |                           Comments                           |
| :--------: | :---------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     4      |   version   |                           int32_t                            |       Block version information (note, this is signed)       |
|     32     | prev_block  |                           char[32]                           | The hash value of the previous block this particular block references |
|     32     | merkle_root |                           char[32]                           | The reference to a Merkle tree collection which is a hash of all transactions related to this block |
|     4      |  timestamp  |                           uint32_t                           | A timestamp recording when this block was created (Will overflow in 2106[[2\]](https://en.bitcoin.it/wiki/Protocol_documentation#cite_note-2)) |
|     4      |    bits     |                           uint32_t                           |  The calculated difficulty target being used for this block  |
|     4      |    nonce    |                           uint32_t                           | The nonce used to generate this block… to allow variations of the header and compute different hashes |
|     1+     |  txn_count  | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |    Number of transaction entries, this value is always 0     |



## tx

*tx* describes a bitcoin transaction.

| Field Size | Description  |                          Data type                           |                           Comments                           |
| :--------: | :----------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     4      |   version    |                           uint32_t                           |               Transaction data format version                |
|   0 or 2   |     flag     |                     optional uint8_t[2]                      | If present, always 0001, and indicates the presence of witness data |
|     1+     | tx_in count  | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |          Number of Transaction inputs (never zero)           |
|    41+     |    tx_in     |                           tx_in[]                            | A list of 1 or more transaction inputs or sources for coins  |
|     1+     | tx_out count | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |                Number of Transaction outputs                 |
|     9+     |    tx_out    |                           tx_out[]                           | A list of 1 or more transaction outputs or destinations for coins |
|     0+     | tx_witnesses |                         tx_witness[]                         | A list of witnesses, one for each input; omitted if *flag* is omitted above |
|     4      |  lock_time   |                           uint32_t                           | The block number or timestamp at which this transaction is unlocked. If all TxIn inputs have final (0xffffffff) sequence numbers then lock_time is irrelevant. Otherwise, the transaction may not be added to a block until after lock_time (see [NLockTime](https://en.bitcoin.it/wiki/NLockTime)).|

### Lock Time Condition

| Value        | Description                                          |
| ------------ | ---------------------------------------------------- |
| 0            | Not locked                                           |
| < 500000000  | Block number at which this transaction is unlocked   |
| >= 500000000 | UNIX timestamp at which this transaction is unlocked |

### TxIn

| Field Size |                       Description                       |                          Data type                           |                           Comments                           |
| :--------: | :-----------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     36     |                     previous_output                     |                           outpoint                           | The previous output transaction reference, as an OutPoint structure |
|     1+     |                      script length                      | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |              The length of the signature script              |
|     ?      |                    signature script                     |                           uchar[]                            | Computational Script for confirming transaction authorization |
|     4      | [sequence](http://bitcoin.stackexchange.com/q/2025/323) |                           uint32_t                           | Transaction version as defined by the sender. Intended for "replacement" of transactions when information is updated before inclusion into a block. |



### TxOut

The TxOut structure consists of the following fields:

| Field Size |   Description    |                          Data type                           |                           Comments                           |
| :--------: | :--------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|     8      |      value       |                           int64_t                            |                      Transaction Value                       |
|     1+     | pk_script length | [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) |                   Length of the pk_script                    |
|     ?      |    pk_script     |                           uchar[]                            | Usually contains the public key as a Bitcoin script setting up conditions to claim this output. |



#### TxWitness

The TxWitness structure consists of a [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) count of witness data components, followed by (for each witness data component) a [var_int](https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer) length of the component and the raw component data itself.



#### Variable length integer(var_int)

Integer can be encoded depending on the represented value to save space. Variable length integers always precede an array/vector of a type of data that may vary in length. Encoded in little endian.

|     Value      | Storage length |                 Format                  |
| :------------: | :------------: | :-------------------------------------: |
|     < 0xFD     |       1        |                 uint8_t                 |
|   <= 0xFFFF    |       3        | 0xFD followed by the length as uint16_t |
| <= 0xFFFF FFFF |       5        | 0xFE followed by the length as uint32_t |
|       -        |       9        | 0xFF followed by the length as uint64_t |

