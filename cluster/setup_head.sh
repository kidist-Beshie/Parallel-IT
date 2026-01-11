#!/bin/bash

# Stop any previous Ray instance
ray stop

# Start Ray head node
ray start --head --port=6379
