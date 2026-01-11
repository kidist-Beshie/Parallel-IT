# Distributed PPO on Grid5000

This project runs distributed PPO training using Ray RLlib on the Grid5000 cluster.

## Structure
- src/: training scripts
- cluster/: Ray cluster setup
- results/: logs, plots, metrics

## How to run
Single node:
    python src/train.py

Multi node:
    python src/train2.py

