# Learning kinesis

This is just my efforts to learn AWS Kinesis. So, initially I just thought of prepping a set of CLI commands wrapped in a Makefile to see how the API works.

## Running the Makefile

### Crating the datastream
 ```
 $ make create
aws kinesis create-stream --stream-name test-stream --shard-count 1
 ```

### Listing the datastream

```
$ make list
aws kinesis list-streams
{
    "StreamNames": [
        "test-stream"
    ]
}
```

### Describing the datastream

```
$ make describe
aws kinesis describe-stream --stream-name test-stream
{
    "StreamDescription": {
        "KeyId": null,
        "EncryptionType": "NONE",
        "StreamStatus": "ACTIVE",
        "StreamName": "test-stream",
        "Shards": [
            {
                "ShardId": "shardId-000000000000",
                "HashKeyRange": {
                    "EndingHashKey": "<REDACTED>",
                    "StartingHashKey": "0"
                },
                "SequenceNumberRange": {
                    "StartingSequenceNumber": "49596470646235019120477111573566540453842319220217479170"
                }
            }
        ],
        "StreamARN": "arn:aws:kinesis:ap-south-1:<REDACTED>:stream/test-stream",
        "EnhancedMonitoring": [
            {
                "ShardLevelMetrics": []
            }
        ],
        "StreamCreationTimestamp": 1559962836.0,
        "RetentionPeriodHours": 24
    }
}
```

### Putting the data to the datastream

Calling the put twice to see multiple data
```
$ cat payload.json
{"x": 20, "y": 30}

$ make put
aws kinesis put-record --stream-name test-stream --data file://payload.json --partition-key 1
{
    "ShardId": "shardId-000000000000",
    "SequenceNumber": "49596470646235019120477111574989446143528745386708566018"
}
```

### Getting the shard-iterator

```
$ make get-id
aws kinesis get-shard-iterator --stream-name test-stream --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON
{
    "ShardIterator": "AAAAAAAAAAERubv/xyMs0Imb39sCZ9kdYUtVMmkUv4eOlAGmsg8STM5T40UOJVh7S3DsJ9UjCYrrXda5+TU/a05sUUmxS9eIN+oeCuEBcWe7vYLPKgVIFvhLpWE1g59/u4nG63Nmk+2TmhcsXRFnvWJC1UzYJnnTu/hrBEfhPxcZMkXpkgs+3txtFJ2Mui1wFg9iwhmDwmQQO5GWrTqB/AJBmtD/lxiX"
```

### Getting the data

```
$ make get
aws kinesis get-records --shard-iterator AAAAAAAAAAERubv/xyMs0Imb39sCZ9kdYUtVMmkUv4eOlAGmsg8STM5T40UOJVh7S3DsJ9UjCYrrXda5+TU/a05sUUmxS9eIN+oeCuEBcWe7vYLPKgVIFvhLpWE1g59/u4nG63Nmk+2TmhcsXRFnvWJC1UzYJnnTu/hrBEfhPxcZMkXpkgs+3txtFJ2Mui1wFg9iwhmDwmQQO5GWrTqB/AJBmtD/lxiX
{
    "Records": [
        {
            "Data": "eyJ4IjogMjAsICJ5IjogMzB9Cg==",
            "PartitionKey": "1",
            "ApproximateArrivalTimestamp": 1559962945.316,
            "SequenceNumber": "49596470646235019120477111574989446143528745386708566018"
        },
        {
            "Data": "eyJ4IjogMjAsICJ5IjogMzB9Cg==",
            "PartitionKey": "1",
            "ApproximateArrivalTimestamp": 1559963086.984,
            "SequenceNumber": "49596470646235019120477111575007580030822974582494855170"
        }
    ],
    "NextShardIterator": "AAAAAAAAAAHp4IVf9jJOgpiRGWXFgSSs1FBzM29U/KO5D4PhbdvbxBdf4/2P8U4CuVwQRfCRKN4XIUrjyT+kKD6GCSvX+DrNCdrDnNpBOh5ZCFwxDv/52P7+7bEWmFeksXV78Ha8wAvjeGYGqczvxcuEKWdltLUchTfpQp1BUFugf2GWcqYxgdyUjyGIKua/3KYgcTr80pQV/ZPesksuwntD/ke5WA6B",
    "MillisBehindLatest": 0
}

$ echo eyJ4IjogMjAsICJ5IjogMzB9Cg== | base64 -D
{"x": 20, "y": 30}
```

### And finally, delete the datastream

```
$ make delete
aws kinesis delete-stream --stream-name test-stream
```
