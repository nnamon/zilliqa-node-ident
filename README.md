# zilliqa-node-ident

Node type identifier for Zilliqa node logs.

```
tail -n 5000 zilliqa-00001-log.txt | python zilliqa-identify.py
```

or

```
python zilliqa-identify.py --logfile zilliqa-00001-log.txt
```

## Node Types

* **normal** - You are a normal non-member of the network. You will have to perform POW on the next DS epoch to bid for membership. No rewards.
* **shard** - You are a member of a shard in the network. You will get rewards.
* **ds** - You are a member of the DS committee. You will get rewards.
* **malfunctioning** - Something is wrong with your node. Restart it.
