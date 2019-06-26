#!/bin/bash

stream_name=$1
REQUEST="What is your name?"
start_time=`date +%s`
request=`echo $REQUEST|base64`
echo $REQUEST
read RESPONSE
end_time=`date +%s`
response=`echo $RESPONSE|base64`
delta=`expr $end_time - $start_time`

data={\"start_time\":$start_time,\"request\":\"$request\",\"response\":\"$response\",\"delta\":$delta}

payload=$data
echo $payload
cmd="aws kinesis put-record --stream-name $stream_name --data $payload --partition-key 1"
echo $cmd
$cmd
