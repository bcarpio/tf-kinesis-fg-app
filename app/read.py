from __future__ import print_function
import sys, os, time
import json
import boto3
from pprint import pprint

class ReadFromStream:

    def read_message(self):
        self.stream = 'dev-rep-kinesis'
        self.shard_id = 'shardId-000000000000'
        self.client = boto3.client('kinesis')

        self.shard_it = self.client.get_shard_iterator(
            StreamName = self.stream,
            ShardId = self.shard_id,
            ShardIteratorType = "LATEST")["ShardIterator"]

        while 1==1:
            self.response = self.client.get_records(
                ShardIterator = self.shard_it,
                Limit = 100
            )
            print(self.response['Records'])
            shard_it = self.response["NextShardIterator"]
            time.sleep(0.2)

if __name__ == "__main__":
    kinesisobject = ReadFromStream()
    pprint(kinesisobject.read_message())
