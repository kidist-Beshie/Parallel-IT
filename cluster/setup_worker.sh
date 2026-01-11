#!/bin/bash

# Usage: bash setup_worker.sh <HEAD-IP>

HEAD_IP=$1

# Stop any previous Ray instance
ray stop

# Connect to the head node
ray start --address="$HEAD_IP:6379"
