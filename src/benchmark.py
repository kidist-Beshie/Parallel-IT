import ray
from ray.rllib.algorithms.ppo import PPOConfig
import time
import os
import json

# --- SETTINGS ---
# Set this manually for each test run
NUM_NODES = 4
WORKER_COUNTS = [2, 4, 8, 12, 24, 32, 48, 64]

os.environ["RAY_DEDUP_LOGS"] = "0"
ray.init(address="auto")

def run_benchmark(num_workers):
    print(f"\n>>> TESTING: {num_workers} workers on {NUM_NODES} nodes")
    config = (
        PPOConfig()
        .environment("CartPole-v1")
        .framework("torch")
        .env_runners(num_env_runners=num_workers, num_cpus_per_env_runner=1)
    )
    algo = config.build()
    
    rewards = []
    start_time = time.time()
    
    for i in range(10):
        result = algo.train()
        r = result.get("env_runners", {}).get("episode_return_mean", 0)
        rewards.append(r)
        print(f"  Iter {i} | Reward: {r:.2f}")
        
    duration = time.time() - start_time
    algo.stop()
    return duration, rewards

# --- EXECUTION ---
# runs for each number of selected workers 10 iteration
run_data = {
    "nodes": NUM_NODES,
    "results": {}
}

for count in WORKER_COUNTS:
    duration, rewards = run_benchmark(count)
    run_data["results"][count] = {
        "time": duration,
        "rewards": rewards
    }

# --- SAVE TO JSON ---
# this section will dump the numbers in a json file to then plot the graph
filename = f"results_{NUM_NODES}nodes.json"
with open(filename, "w") as f:
    json.dump(run_data, f, indent=4)

print(f"\n[SUCCESS] Data saved to {filename}")
ray.shutdown()
