#!/bin/bash

# 1. Download and install Miniconda (if not already there)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
source "$HOME/miniconda/bin/activate"

# 2. Create and activate a specific environment
conda create -y -n rllib_env python=3.10
conda activate rllib_env

# 3. Install RLlib and Gymnasium
$HOME/miniconda/envs/rllib_env/bin/pip install "ray[rllib]" "gymnasium[classic_control]" torch numpy matplotlib

#For information on safely removing channels from your conda configuration,
#please see the official documentation:
#
#    https://www.anaconda.com/docs/tools/working-with-conda/channels
