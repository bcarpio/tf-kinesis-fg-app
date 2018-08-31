import sys, os, time
import json
import boto3
from botocore.exceptions import ClientError
from pprint import pprint


def dump_stream():
    stream = 'dev-rep-kinesis'
    shard_id = 'shardId-000000000000'
    client = boto3.client('kinesis')

    # Grab Initial Shard Iterator
    shard_it = client.get_shard_iterator(
        StreamName = stream,
        ShardId = shard_id,
        ShardIteratorType = "TRIM_HORIZON")["ShardIterator"]

    tries = 0
    records = []
    while tries < 20:
        try:

            # Grab Data For Shard Iterator
            response = client.get_records(
               ShardIterator = shard_it,
                Limit = 100
            )

            for rec in response['Records']:
                record = json.loads(json.loads(rec['Data']))
                try:
                    if record['detail']['responseElements'] is not None:
                        records.append(record['detail'])
                except KeyError:
                    pass

            # Grab Next Shard Iterator for next loop
            shard_it = response['NextShardIterator']
            tries +=1

        # Look for Throughput Exception and Sleep if Hit
        except ClientError as err:
            if err.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                time.sleep(0.5)
            else:
                # End Loop if Some Other Error Occurs
                pprint(err.response)
                break
    return records

def get_instance_data():
    records = dump_stream()
    inst_records = []
    for rec in records:
        try:
            if rec['eventName'] in ('RunInstances', 'TerminateInstances'):
                inst_records.append(rec)
        except KeyError:
            pass
    return inst_records

def get_rds_data():
    records = dump_stream()
    rds_records = []
    for rec in records:
        try:
            if rec['eventName'] in ('CreateDBCluster', 'CreateDBInstance', 'DeleteDBCluster', 'DeleteDBInstance'):
                rds_records.append(rec)
        except KeyError:
            pass
    return rds_records

if __name__ == "__main__":
    get_rds_data()
