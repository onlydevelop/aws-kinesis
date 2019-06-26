stream_name = activity_stream

create:
	aws kinesis create-stream --stream-name $(stream_name) --shard-count 1

delete:
	aws kinesis delete-stream --stream-name $(stream_name)

list:
	aws kinesis list-streams

describe:
	aws kinesis describe-stream --stream-name $(stream_name)

put:
	# aws kinesis put-record --stream-name $(stream_name) --data file://payload.json --partition-key 1
	./ask.sh $(stream_name)

get-id:
	aws kinesis get-shard-iterator --stream-name $(stream_name) --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON

get:
	# Put the shard-iterator value from the get-id response
	aws kinesis get-records --shard-iterator AAAAAAAAAAERubv/xyMs0Imb39sCZ9kdYUtVMmkUv4eOlAGmsg8STM5T40UOJVh7S3DsJ9UjCYrrXda5+TU/a05sUUmxS9eIN+oeCuEBcWe7vYLPKgVIFvhLpWE1g59/u4nG63Nmk+2TmhcsXRFnvWJC1UzYJnnTu/hrBEfhPxcZMkXpkgs+3txtFJ2Mui1wFg9iwhmDwmQQO5GWrTqB/AJBmtD/lxiX
