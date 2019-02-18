#!/usr/bin/env python

import argparse
import sys
import re


SHARD_NODE_PATTERNS = [
        "I am a backup node",
        "I am backup member of the sharded committee",
        "I am shard backup",
        "Node State = ",
        ]

DS_NODE_PATTERNS = [
        "PROCESS_MICROBLOCKSUBMISSION not allowed in FINALBLOCK_CONSENSUS",
        "Received microblock for epoch",
        "Save coin base for",
        "Rewarding",
        "More then expected epoch rewardees",
        "DS microblock consensus already started, ignore this microblock submission",
        "Left reward",
        "Lucky draw winner",
        "I am a backup DS node",
        "DS State = "
        ]

MALFUNCTIONING_NODE_PATTERNS = [
        "The latest DS index does not match that of the latest tx block ds num, try fetching Tx and Dir Blocks again",
        "Even after the recving latest ds info, the information is stale",
        ]

NORMAL_NODE_PATTERNS = [
        "DS State = POW_SUBMISSION",
        "No Directory blocks sent/ I have the latest blocks",
        "The lowBlockNum is higher the highblocknum, maybe DS epoch ongoing"
        "Set sync type to 2",
        ]


def determine_type(line):
    node_types = (("normal", NORMAL_NODE_PATTERNS),
                  ("malfunctioning", MALFUNCTIONING_NODE_PATTERNS),
                  ("ds", DS_NODE_PATTERNS),
                  ("shard", SHARD_NODE_PATTERNS))

    for name, patterns in node_types:
        for pattern in patterns:
            if pattern in line:
                return name

    return None


def identify(data):
    node_type = "normal"
    epoch_pattern = re.compile(r'^.+Epoch number is now (\d+).+$')
    for line in data.split("\n"):
        match = epoch_pattern.match(line)
        if match:
            epoch = int(match.group(1))
            if epoch % 100 == 0:
                node_type = "normal"
        temp_type = determine_type(line)
        if temp_type is not None:
            node_type = temp_type
    return node_type


def main():
    parser = argparse.ArgumentParser(description='Heurestically identify the type of Zilliqa node from a log file.')
    parser.add_argument('--logfile', help="Specify the path to the log file to parse.")
    args = parser.parse_args()

    if args.logfile is not None:
        fd = open(args.logfile)
    else:
        fd = sys.stdin

    data = fd.read()
    print(identify(data))


if __name__ == '__main__':
    main()
